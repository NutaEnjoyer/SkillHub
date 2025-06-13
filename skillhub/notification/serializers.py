from notification.models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification serializer for notifications.

    - `id`: The ID of the notification.
    - `user`: The user to whom the notification is sent.
    - `message`: The message of the notification.
    - `created_at`: The date and time when the notification was created.
    - `sent`: Indicates whether the notification has been sent.
    """

    class Meta:
        model = Notification
        fields = ["id", "user", "message", "created_at", "sent"]
