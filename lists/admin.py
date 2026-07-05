from django.contrib import admin
from .models import List, ListItem


class ListItemInline(admin.TabularInline):
    model = ListItem
    extra = 0
    autocomplete_fields = ("product",)


class ListAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "owner", "is_public", "is_commentable", "created")
    list_filter = ("type", "is_public", "is_commentable", "created")
    search_fields = ("name", "owner__email", "owner__username")
    date_hierarchy = "created"
    inlines = [ListItemInline]


admin.site.register(List, ListAdmin)
