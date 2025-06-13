from core.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema
from notification.models import Notification
from notification.serializers import NotificationSerializer
from notification.tasks import send_notification_email
from rest_framework import viewsets


@extend_schema(tags=["Notification"])
class NotificationViewSet(viewsets.ModelViewSet):
    """
    Endpoint for managing notifications.

    - GET /notifications/: Retrieve a list of all notifications.
    - POST /notifications/: Create a new notification.
    - GET /notifications/{id}/: Retrieve a specific notification by ID.
    - PUT/PATCH /notifications/{id}/: Update a specific notification by ID.
    - DELETE /notifications/{id}/: Delete a specific notification by ID.
    """

    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Customize the queryset to filter notifications based on the authenticated user.
        """

        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        """
        Override the perform_create method to set the user field in the serializer
        and send a notification email asynchronously.
        """

        user_id = self.request.data.get("user")
        serializer.save(user_id=user_id if user_id else self.request.user.id)

        send_notification_email.delay(serializer.instance.id)
