from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from rest_framework import filters
from rest_framework.filters import SearchFilter
from rest_framework.settings import api_settings
from django.utils.translation import gettext_lazy as _

from django_filters import FilterSet, CharFilter, ModelMultipleChoiceFilter, AllValuesFilter

from categories.models import Category
from enterprises.models import Enterprise
from products.models import Product


class CategoryFilter(FilterSet):

    category = CharFilter(method='get_category')

    def get_category(self, queryset, name, value):
        queryset = queryset.filter(products__category__slug=value).distinct()
        return queryset

    # def filter_queryset(self, queryset):

        # return queryset.filter()
    # class Meta:
    #     model = Product
    #     fields = ['category', ]
    #
    # @property
    # def qs(self):
    #     query_set = super().qs()
    #     return

