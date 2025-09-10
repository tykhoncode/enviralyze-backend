from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.db import transaction, IntegrityError
from .models import Profile, Follow
from .serializers import ProfileSerializer
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    @action(detail=True, methods=["post", "delete"])
    def follow(self, request, pk=None):
        me = request.user.profile
        target = self.get_object()

        if request.method == "POST":
            if me.pk == target.pk:
                return Response({"detail": "You cannot follow yourself."},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                with transaction.atomic():
                    obj, created = Follow.objects.get_or_create(
                        follower=me, following=target
                    )
            except IntegrityError:
                created = False
            data = ProfileSerializer(target, context={"request": request}).data
            return Response(data,
                            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        with transaction.atomic():
            Follow.objects.filter(follower=me, following=target).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        profile = self.get_object()
        qs = profile.followers.select_related('user')
        page = self.paginate_queryset(qs)
        ser = ProfileSerializer(page or qs, many=True, context={'request': request})
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        profile = self.get_object()
        qs = profile.following.select_related('user')
        page = self.paginate_queryset(qs)
        ser = ProfileSerializer(page or qs, many=True, context={'request': request})
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=False, methods=["get", "patch"], permission_classes=[permissions.IsAuthenticated], url_path="me")
    def me(self, request):
        me = request.user.profile
        if request.method == "GET":
            return Response(self.get_serializer(me).data)

        ser = self.get_serializer(me, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path="me/followers")
    def my_followers(self, request):
        me = request.user.profile
        qs = me.followers.select_related('user')
        page = self.paginate_queryset(qs)
        ser = ProfileSerializer(page or qs, many=True, context={'request': request})
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path="me/following")
    def my_following(self, request):
        me = request.user.profile
        qs = me.following.select_related('user')
        page = self.paginate_queryset(qs)
        ser = ProfileSerializer(page or qs, many=True, context={'request': request})
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)