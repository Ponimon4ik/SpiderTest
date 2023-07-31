from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from districts.models import CityDistrict
from products.models import Product
from .filters import ProductSearchFilter, CategoryFilter
from .serializers import (
    EnterpriseReadSerializer, ProductReadSerializer, ProductCreateSerializer
)
from .viewsets import CreateRetrieveViewSet


class EnterpriseCityDistrictViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, ProductSearchFilter)
    filterset_class = CategoryFilter
    search_fields = ('product__name', )
    serializer_class = EnterpriseReadSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return CityDistrict.objects.none()
        district = get_object_or_404(
            CityDistrict, id=self.kwargs.get('district_id')
        )
        return district.enterprises.all()


class ProductViewSet(CreateRetrieveViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductReadSerializer
        return ProductCreateSerializer
