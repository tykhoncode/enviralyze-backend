from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_url = f"{settings.BACKEND_URL}/api/verifications/verify/?uid={uid}&token={token}"

    subject = "Verify your account"
    message = f"Hi {user.username},\n\nPlease click the link below to verify your account:\n{verify_url}\n\nIf you didn’t sign up, please ignore this email."

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])