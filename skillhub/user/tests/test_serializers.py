from django.contrib.auth import get_user_model
from django.test import TestCase
from user.serializers import UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="Test User",
        )

    def test_valid_data_serialization(self):
        data = {
            "email": "test2@example.com",
            "full_name": "Test User",
            "password": "strong_password_12",
        }

        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_email(self):
        data = {
            "email": "invalid_email",
            "full_name": "Test User",
            "password": "strong_password_12",
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_serialization_output(self):
        serializer = UserSerializer(instance=self.user)
        expected_data = {
            "id": self.user.id,
            "email": "test@example.com",
            "full_name": "Test User",
            "role": "student",
            "enrolled_courses": [],
        }
        self.assertEqual(serializer.data, expected_data)
