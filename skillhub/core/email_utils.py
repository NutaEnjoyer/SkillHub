from django.conf import settings
from django.core.mail import send_mail


class EmailService:
    def __init__(self, from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
        self.from_email = from_email
        self.fail_silently = fail_silently

    def send(self, subject: str, message: str, to_email: str):
        send_mail(
            subject=subject,
            message=message,
            from_email=self.from_email,
            recipient_list=[to_email],
            fail_silently=self.fail_silently,
        )
