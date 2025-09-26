from rest_framework import serializers
from .models import List, ListItem
from products.models import Product


class ListItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_barcode = serializers.CharField(source="product.barcode", read_only=True)

    class Meta:
        model = ListItem
        fields = ["id", "product", "product_name", "product_barcode", "added_at", "order"]
        read_only_fields = ["id", "added_at"]


class ListSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)
    products = ListItemSerializer(source="items", many=True, read_only=True)

    class Meta:
        model = List
        fields = [
            "id",
            "name",
            "type",
            "is_shared",
            "creator",
            "products",
            "created",
            "updated",
        ]
        read_only_fields = ["id", "creator", "created", "updated"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["creator"] = request.user
        return super().create(validated_data)