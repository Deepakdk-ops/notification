from django.core.mail import send_mail
from django.conf import settings


class EmailBackend:
    def send(self, user_email: str, subject: str, message: str):
        # Use a real provider / integration in production
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=True,
        )