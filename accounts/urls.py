from .views import GetUser
from django.urls import path

urlpatterns = [
    path('', GetUser.as_view()),
]