from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.url = reverse("register")  # Имя маршрута в urls.py
        self.user_data = {
            "email": "test@example.com",
            "password": "strong_password_123",
            "full_name": "TestUser",
        }

    def test_register_user(self):
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(full_name="TestUser").exists())


class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="TestUser",
        )
        self.url = reverse("login")

        self.login_data = {
            "email": "test@example.com",
            "password": "strong_password_12",
        }

    def test_login_user(self):
        response = self.client.post(self.url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh_token", response.cookies)


class UserTokenRefreshTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="TestUser",
        )
        self.url = reverse("token_refresh")

    def test_token_refresh(self):
        _response = self.client.post(
            reverse("login"),
            {"email": "test@example.com", "password": "strong_password_12"},
            format="json",
        )
        refresh_token = _response.cookies["refresh_token"].value
        response = self.client.post(
            self.url, format="json", cookies={"refresh_token": refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh_token", response.cookies)
        self.assertNotEqual(refresh_token, response.cookies["refresh_token"].value)


class UserGetProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="TestUser",
        )
        self.url = reverse("profile")

    def test_get_user_profile_with_no_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["full_name"], "TestUser")
        self.assertEqual(response.data["role"], "student")


class UserUpdateTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="TestUser",
        )
        self.url = reverse("profile")

        self.update_data = {
            "full_name": "UpdatedUser",
        }

        self.client.force_authenticate(user=self.user)

    def test_update_user(self):
        response = self.client.patch(self.url, self.update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["full_name"], "UpdatedUser")
