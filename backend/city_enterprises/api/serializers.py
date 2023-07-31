from django.contrib.postgres.search import TrigramWordSimilarity
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from districts.models import CityDistrict
from enterprises.models import Enterprise
from products.models import Product, ProductPrice, NOT_MATCH_NETWORK


DUPLICATE_PRODUCT = 'Такой продукт уже есть в базе данных'


class ProductPriceWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPrice
        fields = ('price', 'enterprise')


class ProductCreateSerializer(serializers.ModelSerializer):

    prices = ProductPriceWriteSerializer(many=True, required=False)

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

    def validate(self, data):
        product_prices = data.get('prices', ())
        for product_price in product_prices:
            if (
                product_price['enterprise'].enterprise_network !=
                data.get('enterprise_network')
            ):
                raise serializers.ValidationError(NOT_MATCH_NETWORK)
        return data

    def create(self, validated_data):
        product_prices = validated_data.pop('prices', ())
        product = Product.objects.create(**validated_data)
        for product_price in product_prices:
            ProductPrice.objects.create(
                product=product,
                enterprise=product_price['enterprise'],
                price=product_price['price']
            )
        return product

    def to_representation(self, instance):
        return ProductReadSerializer(instance).data


class ProductPriceReadSerializer(serializers.ModelSerializer):

    enterprise = serializers.ReadOnlyField(
        source='enterprise.name'
    )

    class Meta:
        model = ProductPrice
        fields = ('price', 'enterprise')


class ProductReadSerializer(serializers.ModelSerializer):

    prices = ProductPriceReadSerializer(source='products_prices', many=True)
    enterprise_network = serializers.ReadOnlyField(
        source='enterprise_network.name'
    )
    category = serializers.ReadOnlyField(
        source='category.name'
    )

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category',
            'enterprise_network', 'description', 'prices'
        )
        read_only_fields = (
            'id', 'name', 'category',
            'enterprise_network', 'description', 'prices'
        )


class EnterpriseProductReadSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')
    category = serializers.ReadOnlyField(source='product.category.name')

    class Meta:
        model = ProductPrice
        fields = ('id', 'name', 'category', 'price')
        read_only_fields = ('id', 'name', 'category', 'price')


class EnterpriseReadSerializer(serializers.ModelSerializer):

    enterprise_network = serializers.ReadOnlyField(
        source='enterprise_network.name'
    )
    products = EnterpriseProductReadSerializer(
        source='products_prices', many=True
    )
    districts = serializers.SlugRelatedField(
        slug_field='name', queryset=CityDistrict.objects.all(), many=True
    )

    class Meta:
        model = Enterprise
        fields = (
            'id', 'name', 'enterprise_network', 'districts', 'products'
        )
        read_only_fields = (
            'id', 'name', 'enterprise_network', 'districts', 'products'
        )
