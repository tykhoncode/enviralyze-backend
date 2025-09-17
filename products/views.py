from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProductSerializer
from .services.openfoodfacts.sync import get_or_update_if_needed

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