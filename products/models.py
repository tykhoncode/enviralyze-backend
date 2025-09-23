from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment

GTIN_VALIDATOR = RegexValidator(r'^\d{8,14}$', 'Barcode must be 8–14 digits')


class Product(models.Model):
    barcode = models.CharField(max_length=14, unique=True, validators=[GTIN_VALIDATOR])
    name = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)
    sustainability_data = models.JSONField(blank=True, null=True)
    comments = GenericRelation(Comment, related_query_name="product")

    last_checked_at = models.DateTimeField(blank=True, null=True, db_index=True)
    last_synced_at = models.DateTimeField(blank=True, null=True, db_index=True)
    off_last_modified_t = models.DateTimeField(blank=True, null=True)
    off_etag = models.CharField(max_length=255, blank=True, null=True)

    def mark_synced(self, off_last_modified_t=None, etag=None):
        self.last_synced_at = timezone.now()
        self.last_checked_at  = timezone.now()
        if off_last_modified_t:
            self.off_last_modified_t = off_last_modified_t
        if etag is not None:
            self.off_etag = etag

    def mark_checked(self):
        self.last_checked_at = timezone.now()

    def __str__(self):
        return f"{self.name or 'Unnamed'} ({self.barcode})"

class UserProductInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    approved = models.BooleanField(default=None, null=True, blank=True)  # ✅ True = Approved, False = Disapproved, None = No action

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        status = "Approved" if self.approved is True else "Disapproved" if self.approved is False else "Undecided"
        return f"{status} the {self.product.name} by {self.user.email}"