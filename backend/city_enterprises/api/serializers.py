from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from categories.models import Category
from districts.models import CityDistrict
from enterprises.models import Enterprise, EnterpriseNetwork
from products.models import Product


class ProductReadSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'category')
        read_only_fields = ('id', 'name', 'category')


class EnterpriseListSerializer(serializers.ModelSerializer):

    enterprise_network = serializers.SlugRelatedField(
        slug_field='name', queryset=EnterpriseNetwork.objects.all()
    )
    products = ProductReadSerializer(many=True)

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'enterprise_network', 'products')
        read_only_fields = ('id', 'name', 'enterprise_network', 'products')


class EnterpriseRetrieveSerializer(serializers.ModelSerializer):

    enterprise_network = serializers.SlugRelatedField(
        slug_field='name', queryset=EnterpriseNetwork.objects.all()
    )
    products = ProductReadSerializer(many=True)
    districts = serializers.SlugRelatedField(
        slug_field='name', queryset=CityDistrict.objects.all(), many=True
    )

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'enterprise_network', 'districts', 'products')
        read_only_fields = ('id', 'name', 'enterprise_network', 'districts', 'products')
