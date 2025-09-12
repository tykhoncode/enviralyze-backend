from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "barcode", "category")
    search_fields = ('name', 'brand', 'barcode')
    list_filter = ('category',)

admin.site.register(Product, ProductAdmin)