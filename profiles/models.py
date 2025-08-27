from django.db import models
from django.conf import settings

def user_avatar_path(instance, filename):
    return f"user_{instance.user_id}/avatars/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    about = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    darkmode = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)

    def __str__(self):
        return self.user.email