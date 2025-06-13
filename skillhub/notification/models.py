from django.conf import settings
from django.db import models


class Notification(models.Model):
    """
    Notification model for sending notifications to users.

    - `user`: The user to whom the notification is sent.
    - `message`: The message of the notification.
    - `created_at`: The date and time when the notification was created.
    - `sent`: Indicates whether the notification has been sent.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message[:30]}"
