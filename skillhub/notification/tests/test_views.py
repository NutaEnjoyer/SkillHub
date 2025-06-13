from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from notification.models import Notification
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class BaseTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="Test User",
            role="admin",
        )
        self.url = reverse("notification-list")

        self.notification_data = {
            "user": self.user.id,
            "message": "This is a test notification",
        }


class NotificationCreateTest(BaseTest):
    @patch("notification.views.send_notification_email.delay")
    def test_create_notification(self, mocked_task):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.notification_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notification.objects.filter(user=self.user).exists())
        self.assertEqual(
            Notification.objects.get(user=self.user).message,
            "This is a test notification",
        )

        mocked_task.assert_called_once_with(Notification.objects.get(user=self.user).id)


class NotificationListTest(BaseTest):
    @patch("notification.views.send_notification_email.delay")
    def test_list_notifications(self, mocked_task):
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.notification_data, format="json")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.user.id)
        self.assertEqual(response.data[0]["message"], "This is a test notification")
        notification = Notification.objects.get(user=self.user)
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, "This is a test notification")
