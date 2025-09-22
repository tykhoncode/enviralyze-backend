from rest_framework import serializers
from .models import Product, ProductComment, UserProductInteraction

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

class ProductCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductComment
        fields = [
            'id', 'product', 'author', 'text',
            'is_edited', 'created_at', 'updated_at'
        ]
        read_only_fields = ['product', 'author', 'is_edited', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['author'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'text' in validated_data and validated_data['text'] != instance.text:
            validated_data['is_edited'] = True
        return super().update(instance, validated_data)

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