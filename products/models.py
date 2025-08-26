from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name or "Unnamed Product"