from django.conf import settings
from django.core.mail import send_mail


def send_notification_email(subject, message, user):
    email = getattr(user, "email", None)
    profile = getattr(user, "profile", None)
    if not email or profile is None or not getattr(profile, "email_notifications", False):
        return
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=True)
    except Exception:
        pass
