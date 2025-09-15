from django.db import models
from django.core.validators import RegexValidator

GTIN_VALIDATOR = RegexValidator(r'^\d{8,14}$', 'Barcode must be 8–14 digits')


class Product(models.Model):
    barcode = models.CharField(max_length=14, unique=True, validators=[GTIN_VALIDATOR])
    name = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name or "Unnamed Product"