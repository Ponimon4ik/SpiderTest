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

    category = AllValuesFilter(field_name='products__category__slug')

    # class Meta:
    #     model = Product
    #     fields = ['category', ]
    #
    # @property
    # def qs(self):
    #     query_set = super().qs()
    #     return

    #
    #
    # def filter_queryset(self, queryset):
    #     ...