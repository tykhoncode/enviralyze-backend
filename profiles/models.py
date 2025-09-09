from django.db import models
from django.conf import settings
from django.db.models import Q, F

def user_avatar_path(instance, filename):
    return f"user_{instance.user_id}/avatars/{filename}"

class Follow(models.Model):
    follower   = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='following_rel')
    following  = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='followers_rel')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower','following'], name='uniq_follow'),
            models.CheckConstraint(check=~Q(follower=F('following')), name='no_self_follow'),
        ]

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
    following = models.ManyToManyField(
        'self',
        through='Follow',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return self.user.email