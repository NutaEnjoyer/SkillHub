from celery import shared_task
from django.core.mail import send_mail
from notification.models import Notification
from django.core.exceptions import ObjectDoesNotExist
from celery.utils.log import get_task_logger
from django.conf import settings


logger = get_task_logger(__name__)


@shared_task
def send_notification_email(notification_id):
    logger.info(
        f"Sending notification email for notification with id {notification_id}"
    )
    try:
        notification = Notification.objects.get(id=notification_id)

        send_mail(
            subject="notification.title",
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.user.email],
            fail_silently=False,
        )

        notification.sent = True
        notification.save()

        logger.info(
            f"Notification email sent successfully for notification with id {notification_id}"
        )

    except ObjectDoesNotExist:
        logger.error(f"Notification with id {notification_id} does not exist")
    except Exception as e:
        logger.error(f"Error sending notification email: {e}")
