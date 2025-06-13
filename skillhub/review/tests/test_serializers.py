from course.models import Category, Course
from django.contrib.auth import get_user_model
from django.test import TestCase
from review.models import Review
from review.serializers import ReviewSerializer

User = get_user_model()


class ReviewSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="Test User",
        )
        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(
            author=self.user,
            title="Course",
            description="Description",
            category=self.category,
            level="beginner",
        )

    def test_valid_data_serialization(self):
        data = {
            "course_id": self.course.id,
            "rating": 5,
            "title": "Great!",
            "content": "Awesome course!",
        }

        serializer = ReviewSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_rating(self):
        data = {
            "course_id": self.course.id,
            "rating": 10,
            "title": "Too much",
            "content": "Nope",
        }

        serializer = ReviewSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("rating", serializer.errors)

    def test_serialization_output(self):
        review = Review.objects.create(
            user=self.user,
            course=self.course,
            rating=5,
            title="Nice",
            content="Well done",
        )

        serializer = ReviewSerializer(review)
        self.assertEqual(serializer.data["rating"], 5)
        self.assertEqual(serializer.data["title"], "Nice")
        self.assertEqual(serializer.data["content"], "Well done")
        self.assertEqual(serializer.data["user"], str(self.user))
        self.assertEqual(serializer.data["course"]["title"], self.course.title)
