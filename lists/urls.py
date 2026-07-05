from rest_framework_nested import routers
from .views import ListViewSet, ListItemViewSet
from comments.views import CommentViewSet

router = routers.DefaultRouter()
router.register(r"lists", ListViewSet, basename="list")

lists_router = routers.NestedDefaultRouter(router, r"lists", lookup="list")
lists_router.register(r"products", ListItemViewSet, basename="list-products")
lists_router.register(r"comments", CommentViewSet, basename="list-comments")

urlpatterns = router.urls + lists_router.urls