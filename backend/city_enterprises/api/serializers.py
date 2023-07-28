from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from categories.models import Category
from districts.models import CityDistrict
from enterprises.models import Enterprise, EnterpriseNetwork
from products.models import Product, ProductPrice


class ProductReadSerializer(serializers.ModelSerializer):

    id = serializers.SlugRelatedField(
        source='product', slug_field='id', queryset=Product.objects.all()
    )
    name = serializers.ReadOnlyField(source='product.name')
    category = serializers.SlugRelatedField(
        source='product.category', slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = ProductPrice
        fields = ('id', 'name', 'category', 'price')
        read_only_fields = ('id', 'name', 'category', 'price')


class EnterpriseListSerializer(serializers.ModelSerializer):

    enterprise_network = serializers.SlugRelatedField(
        slug_field='name', queryset=EnterpriseNetwork.objects.all()
    )
    products = ProductReadSerializer(source='products_prices', many=True)

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'enterprise_network', 'products')
        read_only_fields = ('id', 'name', 'enterprise_network', 'products')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        category_slug = self.context['request'].query_params.get('category')
        if category_slug:
            products = instance.products_prices.filter(product__category__slug=category_slug)
            representation['products'] = ProductReadSerializer(products, many=True).data
        return representation


class EnterpriseRetrieveSerializer(serializers.ModelSerializer):

    enterprise_network = serializers.SlugRelatedField(
        slug_field='name', queryset=EnterpriseNetwork.objects.all()
    )
    products = ProductReadSerializer(source='products_prices', many=True)
    districts = serializers.SlugRelatedField(
        slug_field='name', queryset=CityDistrict.objects.all(), many=True
    )

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'enterprise_network', 'districts', 'products')
        read_only_fields = ('id', 'name', 'enterprise_network', 'districts', 'products')
