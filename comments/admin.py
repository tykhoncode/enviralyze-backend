from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "content_object", "short_text", "created_at", "is_edited")
    list_filter = ("is_edited", "created_at", "content_type")
    search_fields = ("text", "author__email", "author__username")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "short_text")

    def short_text(self, obj):
        return (obj.text[:50] + "...") if len(obj.text) > 50 else obj.text
    short_text.short_description = "Text"

admin.site.register(Comment, CommentAdmin)
