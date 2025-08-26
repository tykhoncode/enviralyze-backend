from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.response import Response

User = get_user_model()


# Create your views here.
class GetUser(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        user = User.objects.first()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
