from django.shortcuts import get_object_or_404
from .models import Product, ProductComment
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProductSerializer, ProductCommentSerializer
from .services.openfoodfacts.sync import get_or_update_if_needed
from core.permissions import IsAuthorOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    lookup_field = "barcode"
    lookup_value_regex = r"\d{8,14}"

    @action(detail=False, methods=["post"], url_path=r"sync/(?P<barcode>\d{8,14})")
    def sync_barcode(self, request, barcode=None):

        refresh_flag = str(request.query_params.get("refresh", "0")).lower()
        force = refresh_flag in {"1", "true", "yes", "y"}

        prod = get_or_update_if_needed(barcode, force=force)
        if not prod:
            return Response({"detail": "Not found on Open Food Facts"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(prod).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, barcode=None):
        product = self.get_object()

        if request.method == "GET":
            qs = ProductComment.objects.filter(product=product).select_related("author")
            page = self.paginate_queryset(qs)
            ser = ProductCommentSerializer(page or qs, many=True, context={'request': request})
            return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        ser = ProductCommentSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save(product=product)
        return Response(ser.data, status=status.HTTP_201_CREATED)

class ProductCommentViewSet(viewsets.ModelViewSet):
    queryset = ProductComment.objects.select_related("author", "product")
    serializer_class = ProductCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]