from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment
from products.models import Product

class List(models.Model):
    LIST_TYPES = [
        ("custom", "Custom"),
        ("favorite", "Favorite"),
        ("compare", "Comparison"),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=LIST_TYPES, default="custom")
    data = models.JSONField()
    is_commentable = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lists")
    products = models.ManyToManyField(
        Product,
        through="ListItem",
        related_name="lists",
    )
    comments = GenericRelation(Comment, related_query_name="list")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        unique_together = ("creator", "name", "type")

    def __str__(self):
        return f"{self.name} ({self.type})"

class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("list", "product")
        ordering = ["order", "-added_at"]

    def __str__(self):
        return f"{self.product.name} in {self.list.name}"