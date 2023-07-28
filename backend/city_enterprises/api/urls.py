from django.urls import path, include
from rest_framework import routers

from .views import EnterpriseCityDistrictViewSet, ProductViewSet

ENTERPRISE_URL = r'districts/(?P<district_id>\d+)/organizations'

router_v1 = routers.DefaultRouter()
router_v1.register(ENTERPRISE_URL, EnterpriseCityDistrictViewSet, basename='organization')
router_v1.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
