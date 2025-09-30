from rest_framework_nested import routers
from .views import ListViewSet, ListItemViewSet

router = routers.DefaultRouter()
router.register(r"lists", ListViewSet, basename="list")

lists_router = routers.NestedDefaultRouter(router, r"lists", lookup="list")
lists_router.register(r"products", ListItemViewSet, basename="list-products")

urlpatterns = router.urls + lists_router.urls