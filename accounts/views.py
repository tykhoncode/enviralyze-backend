from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# Create your views here.
class GetUser(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "refresh token is required"}, status=400)
        try:
            RefreshToken(refresh).blacklist()
        except Exception:
            return Response({"detail": "invalid refresh token"}, status=400)
        return Response(status=status.HTTP_205_RESET_CONTENT)
