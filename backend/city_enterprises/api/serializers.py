from django.contrib.postgres.search import TrigramWordSimilarity
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from categories.models import Category
from districts.models import CityDistrict
from enterprises.models import Enterprise, EnterpriseNetwork
from products.models import Product, ProductPrice


DUPLICATE_PRODUCT = 'Такой продукт уже есть в базе данных'


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['enterprises']
        validators = [
            UniqueTogetherValidator(
                queryset=Product.objects.all(),
                fields=['name', 'category', 'enterprise_network'],
                message=DUPLICATE_PRODUCT
            )
        ]

    def to_representation(self, instance):
        return ProductReadSerializer(instance).data


class ProductPriceSerializer(serializers.ModelSerializer):

    enterprise = serializers.ReadOnlyField(
        source='enterprise.name'
    )

    class Meta:
        model = ProductPrice
        fields = ('price', 'enterprise')

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'enterprise_network', 'prices')
        read_only_fields = ('id', 'name', 'category', 'enterprise_network', 'prices')


class ProductReadSerializer(serializers.ModelSerializer):

    prices = ProductPriceSerializer(many=True, source='products_prices')
    enterprise_network = serializers.ReadOnlyField(
        source='enterprise_network.name'
    )
    category = serializers.ReadOnlyField(
        source='category.name'
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'enterprise_network', 'prices')
        read_only_fields = ('id', 'name', 'category', 'enterprise_network', 'prices')


class EnterpriseProductReadSerializer(serializers.ModelSerializer):

    id = serializers.SlugRelatedField(
        source='product', slug_field='id', queryset=Product.objects.all()
    )
    name = serializers.SlugRelatedField(
        source='product', slug_field='name', queryset=Product.objects.all()
    )
    category = serializers.SlugRelatedField(
        source='product.category', slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = ProductPrice
        fields = ('id', 'name', 'category', 'price')
        read_only_fields = ('id', 'name', 'category', 'price')


class EnterpriseReadSerializer(serializers.ModelSerializer):

    enterprise_network = serializers.ReadOnlyField(source='enterprise_network.name',)
    products = EnterpriseProductReadSerializer(source='products_prices', many=True)
    districts = serializers.SlugRelatedField(
        slug_field='name', queryset=CityDistrict.objects.all(), many=True
    )

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'enterprise_network', 'districts', 'products')
        read_only_fields = ('id', 'name', 'enterprise_network', 'districts', 'products')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        search_term = self.context['request'].query_params.get('search')
        category_slug = self.context['request'].query_params.get('category')
        products = instance.products_prices
        if category_slug:
            products = products.filter(product__category__slug=category_slug)
        if search_term:
            products = products.annotate(
                similarity=TrigramWordSimilarity(search_term, 'product__name')
            ).filter(similarity__gte=0.3).order_by('id')
        representation['products'] = EnterpriseProductReadSerializer(products, many=True).data
        return representation

