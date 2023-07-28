from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, viewsets

from api.filters import CategoryFilter, ProductSearchFilter


class CreateRetrieveViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass
