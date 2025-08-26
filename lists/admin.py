from django.contrib import admin
from .models import List

# Register your models here.
class ListAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)

admin.site.register(List)