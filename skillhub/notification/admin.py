from django.contrib import admin
from notification.models import Notification
from notification.tasks import send_notification_email


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Custom admin class for managing notifications.

    Display the notification's ID, user, message, created_at, sent
    Filter by created_at and sent status.
    Search by user's email and message.
    """

    list_display = ("id", "user", "message", "created_at", "sent")
    list_filter = ("created_at", "sent")
    search_fields = ("user__email", "message")
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        """
        Expand the save_model method to send the notification email
        """

        super().save_model(request, obj, form, change)

        if not change:
            send_notification_email.delay(obj.id)
