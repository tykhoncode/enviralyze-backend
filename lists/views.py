from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
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

    def _visible_list(self):
        user = self.request.user
        visible = models.Q(is_public=True)
        if user.is_authenticated:
            visible |= models.Q(owner=user)
        return get_object_or_404(List.objects.filter(visible), pk=self.kwargs["list_pk"])

    def get_queryset(self):
        parent = self._visible_list()
        return ListItem.objects.filter(list=parent).select_related("product")

    def perform_create(self, serializer):
        parent = self._visible_list()
        if parent.owner_id != self.request.user.id and not self.request.user.is_staff:
            raise PermissionDenied("You can only modify your own lists.")
        serializer.save(list=parent)