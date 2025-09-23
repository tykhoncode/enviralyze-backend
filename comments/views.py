from rest_framework import viewsets, permissions
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from core.permissions import IsAuthorOrReadOnly
from .models import Comment
from .serializers import CommentSerializer
from products.models import Product


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related("author")
        if "product_barcode" in self.kwargs:
            product = get_object_or_404(Product, barcode=self.kwargs["product_barcode"])
            return qs.filter(
                content_type=ContentType.objects.get_for_model(Product),
                object_id=product.id,
            )
        return qs.none()

    def perform_create(self, serializer):
        product = get_object_or_404(Product, barcode=self.kwargs["product_barcode"])
        serializer.save(
            author=self.request.user,
            content_type=ContentType.objects.get_for_model(Product),
            object_id=product.id,
        )