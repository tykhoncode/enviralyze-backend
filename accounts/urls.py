from .views import GetUser, RegisterView, LogoutView
from django.urls import path
from .social_views import GoogleLogin

urlpatterns = [
    path('', GetUser.as_view()),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("social/google/", GoogleLogin.as_view(), name="google-login"),
]