from .views import GetUser, RegisterView, LogoutView
from django.urls import path

urlpatterns = [
    path('', GetUser.as_view()),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]