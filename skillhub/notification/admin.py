from django.contrib import admin
from notification.models import Notification
from notification.tasks import send_notification_email


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at", "sent")
    list_filter = ("created_at", "sent")
    search_fields = ("user__username", "message")
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            send_notification_email.delay(obj.id)
