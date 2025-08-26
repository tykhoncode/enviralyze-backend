from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "barcode", "category")

admin.site.register(Product, ProductAdmin)