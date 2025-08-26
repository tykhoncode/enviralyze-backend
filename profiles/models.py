from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    about = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    darkmode = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email