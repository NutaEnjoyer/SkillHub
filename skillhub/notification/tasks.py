from celery import shared_task
from celery.utils.log import get_task_logger
from core.email_utils import EmailService
from django.core.exceptions import ObjectDoesNotExist
from notification.models import Notification

logger = get_task_logger(__name__)

email_service = EmailService()


@shared_task
def send_notification_email(notification_id):
    logger.info(
        f"Sending notification email for notification with id {notification_id}"
    )
    try:
        notification = Notification.objects.get(id=notification_id)

        email_service.send(
            subject="notification.title",
            message=notification.message,
            to_email=notification.user.email,
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
