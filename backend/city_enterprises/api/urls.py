from django.urls import path, include
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import EnterpriseCityDistrictViewSet, ProductViewSet


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

ENTERPRISE_URL = r'districts/(?P<district_id>\d+)/organizations'

router_v1 = routers.DefaultRouter()
router_v1.register(
    ENTERPRISE_URL,
    EnterpriseCityDistrictViewSet, basename='organization'
)
router_v1.register('products', ProductViewSet, basename='product')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

urlpatterns += [
   path(
       'v1/swagger<format>/',
       schema_view.without_ui(cache_timeout=0),
       name='schema-json'
   ),
   path(
       'v1/swagger/',
       schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'
   ),
   path(
       'v1/redoc/',
       schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'
   ),
]
