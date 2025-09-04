from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.urls import reverse

class BackendAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        base = getattr(settings, "BACKEND_URL", "http://localhost:8000").rstrip("/")
        return f"{base}{reverse('account_confirm_email', args=[emailconfirmation.key])}"