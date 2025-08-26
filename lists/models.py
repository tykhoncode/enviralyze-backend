from django.conf import settings
from django.db import models

class List(models.Model):
    name = models.CharField(max_length=255)
    data = models.JSONField()
    is_commentable = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="custom_lists")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'List named {self.name}'