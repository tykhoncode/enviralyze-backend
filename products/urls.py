from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ProductViewSet
from comments.views import CommentViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

products_router = NestedDefaultRouter(router, r"products", lookup="product")
products_router.register(r"comments", CommentViewSet, basename="product-comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
]