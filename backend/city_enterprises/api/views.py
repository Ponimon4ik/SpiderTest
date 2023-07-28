from django_filters.rest_framework import DjangoFilterBackend

from enterprises.models import Enterprise
from products.models import Product
from .filters import ProductSearchFilter, CategoryFilter
from .serializers import EnterpriseReadSerializer, ProductReadSerializer, ProductCreateSerializer
from .viewsets import CreateRetrieveViewSet
from rest_framework import viewsets


class EnterpriseCityDistrictViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, ProductSearchFilter)
    filterset_class = CategoryFilter
    search_fields = ('products__name',)
    serializer_class = EnterpriseReadSerializer

    def get_queryset(self):
        district_id = self.kwargs['district_id']
        queryset = Enterprise.objects.filter(districts__id=district_id)
        return queryset


class ProductViewSet(CreateRetrieveViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductReadSerializer
        return ProductCreateSerializer
