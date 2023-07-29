from django.contrib.postgres.search import TrigramWordSimilarity
from rest_framework.filters import SearchFilter


from django_filters import FilterSet, CharFilter


class CategoryFilter(FilterSet):

    category = CharFilter(field_name='products__category__slug')

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.distinct()


class ProductSearchFilter(SearchFilter):

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset
        search_fields = self.get_search_fields(view, request)
        queryset = queryset.annotate(
            similarity=TrigramWordSimilarity(
                ' '.join(search_terms), search_fields[0]
            )
        ).filter(similarity__gte=0.3).order_by('id')
        return queryset.distinct('id')
