import factory

from categories.models import Category
from districts.models import CityDistrict
from enterprises.models import EnterpriseNetwork, Enterprise
from products.models import Product, ProductPrice


class CityDistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CityDistrict

    name = factory.Faker('street_address')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    slug = factory.Faker('slug')


class EnterpriseNetworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EnterpriseNetwork

    name = factory.Faker('company')


class EnterpriseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enterprise
        skip_postgeneration_save = True

    name = factory.Faker('company')
    enterprise_network = factory.SubFactory(EnterpriseNetworkFactory)

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

    name = factory.Sequence(lambda n: 'product{}'.format(n))
    category = factory.SubFactory(CategoryFactory)
    enterprise_network = factory.SubFactory(EnterpriseNetworkFactory)


class ProductPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPrice

    product = factory.SubFactory(ProductFactory)
    enterprise = factory.SubFactory(EnterpriseFactory)
    price = factory.Faker(
        'pydecimal', right_digits=2, positive=True,
        min_value=1, max_value=1000000
    )


pytest_plugins = [
    'tests.fixtures.fixture_user',
    'tests.fixtures.fixture_data',
]
