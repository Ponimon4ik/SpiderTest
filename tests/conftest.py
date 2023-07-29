from factory import Faker, SubFactory
import factory

from categories.models import Category
from districts.models import CityDistrict
from enterprises.models import EnterpriseNetwork, Enterprise
from products.models import Product, ProductPrice


class CityDistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CityDistrict

    name = Faker('street_address')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker('word')
    slug = Faker('slug')


class EnterpriseNetworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EnterpriseNetwork

    name = Faker('company')


class EnterpriseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enterprise
        skip_postgeneration_save = True

    name = Faker('company')
    enterprise_network = SubFactory(EnterpriseNetworkFactory)

    @factory.post_generation
    def districts(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for district in extracted:
                self.districts.add(district)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker('word')
    category = SubFactory(CategoryFactory)
    enterprise_network = SubFactory(EnterpriseNetworkFactory)


class ProductPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPrice

    product = SubFactory(ProductFactory)
    enterprise = SubFactory(EnterpriseFactory)
    price = Faker('pydecimal', right_digits=2, positive=True, min_value=1, max_value=1000000)


pytest_plugins = [
    'tests.fixtures.fixture_user',
    'tests.fixtures.fixture_data',
]
