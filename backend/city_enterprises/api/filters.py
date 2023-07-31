from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import Prefetch
from rest_framework.filters import SearchFilter


from django_filters import FilterSet, CharFilter

from products.models import ProductPrice


class CategoryFilter(FilterSet):

    category = CharFilter()

    def filter_queryset(self, queryset):
        search_term = self.request.query_params.get('search')
        category_slug = self.request.query_params.get('category')
        if category_slug and search_term or not category_slug:
            return queryset
        products_filter = ProductPrice.objects.filter(
            product__category__slug=category_slug
        )
        return queryset.filter(products_prices__in=products_filter).prefetch_related(
            Prefetch('products_prices', queryset=products_filter)).order_by('id').distinct('id')


class ProductSearchFilter(SearchFilter):

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset
        search_fields = self.get_search_fields(view, request)
        filters = {'similarity__gte': 0.5}
        category_slug = request.query_params.get('category')
        if category_slug:
            filters['product__category__slug'] = category_slug
        products_filter = ProductPrice.objects.annotate(
                    similarity=TrigramWordSimilarity(' '.join(search_terms), search_fields[0])
                ).filter(**filters).order_by('id')
        queryset = queryset.filter(products_prices__in=products_filter).prefetch_related(
            Prefetch('products_prices', queryset=products_filter)).order_by('id')
        return queryset.distinct('id')
