from django.contrib import admin
from .models import Profile, Follow

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'darkmode', "avatar", "followers_count", "following_count")
    search_fields = ("user__email", "user__username")

    def followers_count(self, obj):
        return obj.followers.count()
    followers_count.short_description = "Followers"

    def following_count(self, obj):
        return obj.following.count()
    following_count.short_description = "Following"

class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following", "created_at")

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)
