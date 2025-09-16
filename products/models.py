from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

GTIN_VALIDATOR = RegexValidator(r'^\d{8,14}$', 'Barcode must be 8–14 digits')


class Product(models.Model):
    barcode = models.CharField(max_length=14, unique=True, validators=[GTIN_VALIDATOR])
    name = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    last_synced_at = models.DateTimeField(blank=True, null=True)
    off_last_modified_t = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)
    sustainability_data = models.JSONField(blank=True, null=True)

    def mark_synced(self, off_last_modified_t=None):
        self.last_synced_at = timezone.now()
        if off_last_modified_t:
            self.off_last_modified_t = off_last_modified_t

    def __str__(self):
        return self.name or "Unnamed Product"