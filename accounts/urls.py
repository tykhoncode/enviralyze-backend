from .views import GetUser, LogoutView
from django.urls import path
from .social_views import GoogleLogin

urlpatterns = [
    path('', GetUser.as_view()),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("social/google/", GoogleLogin.as_view(), name="google-login"),
]