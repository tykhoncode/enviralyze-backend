from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, ProductCommentViewSet

router = SimpleRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"product-comments", ProductCommentViewSet, basename="product-comment")

urlpatterns = [
    path("", include(router.urls)),
]