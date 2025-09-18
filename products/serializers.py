from rest_framework import serializers
from .models import Product, ProductComment

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

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