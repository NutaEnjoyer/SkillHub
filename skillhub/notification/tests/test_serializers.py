from django.contrib.auth import get_user_model
from django.test import TestCase
from notification.models import Notification
from notification.serializers import NotificationSerializer

User = get_user_model()


class NotificationSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="Test User",
        )

    def test_valid_data_serialization(self):
        data = {
            "user": self.user.id,
            "message": "This is a test notification",
        }

        serializer = NotificationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["user"], self.user)
        self.assertEqual(
            serializer.validated_data["message"], "This is a test notification"
        )

    def test_invalid_data_serialization(self):
        data = {
            "user": 120,
            "message": "This is test notification",
        }
        serializer = NotificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)

    def test_serialization_output(self):
        notification = Notification.objects.create(
            user=self.user,
            message="This is a test notification",
        )
        serializer = NotificationSerializer(notification)
        self.assertEqual(serializer.data["user"], self.user.id)
        self.assertEqual(serializer.data["message"], "This is a test notification")
        self.assertIn(
            notification.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            serializer.data["created_at"],
        )
