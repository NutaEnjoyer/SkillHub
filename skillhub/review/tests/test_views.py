from course.models import Category, Course
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from review.models import Review

User = get_user_model()


class BaseTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="TestUser",
        )

        self.category = Category.objects.create(name="Test Category")

        self.course = Course.objects.create(
            author=self.user,
            title="Test Course",
            description="Test Description",
            category=self.category,
            level="beginner",
        )

        self.url = reverse("review-list")

        self.review_data = {
            "course_id": self.course.id,
            "rating": 5,
            "title": "Great course!",
            "content": "Great course!",
        }


class ReviewCreateTest(BaseTest):
    def test_create_review(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.review_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Review.objects.filter(user=self.user).exists())
        self.assertEqual(Review.objects.get(user=self.user).rating, 5)
        self.assertEqual(Review.objects.get(user=self.user).course, self.course)
        self.assertEqual(Review.objects.get(user=self.user).content, "Great course!")

    def test_invalid_rating_review(self):
        review_data = {
            "course_id": self.course.id,
            "rating": 6,
            "title": "Great course!",
            "content": "Great course!",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, review_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Review.objects.filter(user=self.user).exists())

    def test_create_review_unauthenticated(self):
        response = self.client.post(self.url, self.review_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewListTest(BaseTest):
    def test_list_reviews(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.review_data, format="json")

        response = self.client.get(self.url)

        print(f"response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["rating"], 5)
        self.assertEqual(response.data[0]["title"], "Great course!")
        self.assertEqual(response.data[0]["content"], "Great course!")
        self.assertEqual(response.data[0]["user"], str(self.user))
        self.assertEqual(response.data[0]["course"]["title"], self.course.title)

    def test_get_review(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.review_data, format="json")

        self.url = reverse("review-detail", args=[response.data["id"]])

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["title"], "Great course!")
        self.assertEqual(response.data["content"], "Great course!")
        self.assertEqual(response.data["user"], str(self.user))
        self.assertEqual(response.data["course"]["title"], self.course.title)
        self.assertEqual(response.data["course"]["id"], self.course.id)
