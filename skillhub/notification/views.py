from core.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema
from notification.models import Notification
from notification.serializers import NotificationSerializer
from notification.tasks import send_notification_email
from rest_framework import viewsets


@extend_schema(tags=["Notification"])
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        user_id = self.request.data.get("user")
        serializer.save(user_id=user_id if user_id else self.request.user.id)

        send_notification_email.delay(serializer.instance.id)
