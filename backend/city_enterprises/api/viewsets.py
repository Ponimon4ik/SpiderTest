from rest_framework import mixins, viewsets


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class CreateRetrieveViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass
