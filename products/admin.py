from django.contrib import admin
from .models import Product, UserProductInteraction


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "barcode", "category")
    search_fields = ('name', 'brand', 'barcode')
    list_filter = ('category',)


class UserProductInteractionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "approved")
    list_filter = ("approved",)
    search_fields = ("user__email", "user__username", "product__name", "product__barcode")


admin.site.register(Product, ProductAdmin)
admin.site.register(UserProductInteraction, UserProductInteractionAdmin)
