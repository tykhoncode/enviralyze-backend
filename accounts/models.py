from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def create_user(self, email=None, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)

        if not username:
            base_username = email.split("@")[0]
            username = base_username
            counter = 99
            while self.model.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

        return super().create_user(username=username, email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email