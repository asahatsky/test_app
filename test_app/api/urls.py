from rest_framework.routers import DefaultRouter
from .viewsets import BuildingViewSet, ItemViewSet, PatentViewSet, CompanyViewSet

router = DefaultRouter()


router.register(r'buildings', BuildingViewSet)
router.register(r'items', ItemViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'patents', PatentViewSet)

urlpatterns = router.urls
