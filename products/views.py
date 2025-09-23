from django.shortcuts import get_object_or_404
from .models import Product, UserProductInteraction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProductSerializer, UserProductInteractionSerializer
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

    @action(detail=True, methods=["post"], url_path="vote")
    def vote(self, request, barcode=None):
        product = self.get_object()
        serializer = UserProductInteractionSerializer(
            data={**request.data, "product": product.id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        interaction = serializer.save()
        return Response(
            UserProductInteractionSerializer(interaction).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="votes")
    def votes(self, request, barcode=None):
        product = self.get_object()
        return Response({
            "approvals": product.userproductinteraction_set.filter(approved=True).count(),
            "disapprovals": product.userproductinteraction_set.filter(approved=False).count(),
        })