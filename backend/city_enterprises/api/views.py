from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from enterprises.models import Enterprise
from .filters import CategoryFilter
# from .filters import CategoryFilter
from .serializers import EnterpriseListSerializer, EnterpriseRetrieveSerializer
from .viewsets import ListRetrieveViewSet, CreateRetrieveViewSet


class EnterpriseCityDistrictViewSet(ListRetrieveViewSet):

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EnterpriseRetrieveSerializer
        return EnterpriseListSerializer

    def get_queryset(self):
        district_id = self.kwargs['district_id']
        queryset = Enterprise.objects.filter(districts__id=district_id)
        return queryset
