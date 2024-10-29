from rest_framework.routers import DefaultRouter
from .apps import SalesNetworkConfig
from .views import NetworkNodeViewSet


app_name = SalesNetworkConfig.name

router = DefaultRouter()
router.register(r'suppliers', NetworkNodeViewSet, basename='suppliers')

urlpatterns = [

] + router.urls
