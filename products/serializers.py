from rest_framework import serializers
from .models import Product, UserProductInteraction

class ProductSerializer(serializers.ModelSerializer):
    approval_count = serializers.SerializerMethodField()
    disapproval_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_approval_count(self, obj):
        return UserProductInteraction.objects.filter(product=obj, approved=True).count()

    def get_disapproval_count(self, obj):
        return UserProductInteraction.objects.filter(product=obj, approved=False).count()

class UserProductInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductInteraction
        fields = ["id", "product", "approved"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        obj, _ = UserProductInteraction.objects.update_or_create(
            user=user,
            product=validated_data["product"],
            defaults={"approved": validated_data.get("approved")},
        )
        return obj