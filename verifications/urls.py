from django.urls import path
from .views import VerifyEmailView

urlpatterns = [
    path("verify/", VerifyEmailView.as_view(), name="verify-email"),
]