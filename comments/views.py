from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from core.permissions import IsAuthorOrReadOnly
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def _get_parent(self):
        if "product_barcode" in self.kwargs:
            from products.models import Product
            return get_object_or_404(Product, barcode=self.kwargs["product_barcode"])
        if "list_pk" in self.kwargs:
            from lists.models import List
            return get_object_or_404(List, pk=self.kwargs["list_pk"])
        return None

    def get_queryset(self):
        qs = Comment.objects.select_related("author")
        parent = self._get_parent()
        if parent is None:
            return qs.none()
        return qs.filter(
            content_type=ContentType.objects.get_for_model(type(parent)),
            object_id=parent.id,
        )

    def perform_create(self, serializer):
        parent = self._get_parent()
        if parent is None:
            raise PermissionDenied("Unknown comment target.")
        if hasattr(parent, "is_commentable") and not parent.is_commentable:
            raise PermissionDenied("Comments are disabled for this list.")
        serializer.save(
            author=self.request.user,
            content_type=ContentType.objects.get_for_model(type(parent)),
            object_id=parent.id,
        )
