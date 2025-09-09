from rest_framework import serializers
from .models import Profile
from django.db.models import Count

class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'about', 'language', 'darkmode', 'avatar', 'followers_count', 'following_count']

queryset = (
    Profile.objects.select_related('user')
    .annotate(
        followers_count=Count('followers', distinct=True),
        following_count=Count('following', distinct=True),
    )
)