from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import List, ListItem
from .serializers import ListSerializer, ListItemSerializer
from core.permissions import IsOwnerOrReadOnly
from products.models import Product
from django.db import models

class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all().select_related("owner").prefetch_related("items__product")
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return List.objects.filter(
                models.Q(owner=user) | models.Q(is_public=True)
            ).select_related("owner").prefetch_related("items__product")
        else:
            return List.objects.filter(is_public=True).select_related("owner").prefetch_related("items__product")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListItemViewSet(viewsets.ModelViewSet):
    serializer_class = ListItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return ListItem.objects.filter(list_id=self.kwargs["list_pk"]).select_related("product")

    def perform_create(self, serializer):
        list_obj = List.objects.get(pk=self.kwargs["list_pk"])
        serializer.save(list=list_obj)