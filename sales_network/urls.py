from django.urls import path

from .apps import SalesNetworkConfig
from .views import index

app_name = SalesNetworkConfig.name

urlpatterns = [
    path("", index, name="index"),
]