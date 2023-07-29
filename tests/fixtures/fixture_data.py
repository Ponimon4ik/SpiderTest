import pytest

from tests.conftest import (
    CityDistrictFactory, CategoryFactory, EnterpriseFactory,
    EnterpriseNetworkFactory, ProductFactory, ProductPriceFactory
)


@pytest.fixture
def districts():
    return CityDistrictFactory.create_batch(3)


@pytest.fixture
def categories():
    return CategoryFactory.create_batch(3)


@pytest.fixture
def enterprise_networks():
    return EnterpriseNetworkFactory.create_batch(2)


@pytest.fixture
def network_enterprises(districts, enterprise_networks):
    enterprises = EnterpriseFactory.create_batch(
            2, enterprise_network=enterprise_networks[0]
    )
    for enterprise in enterprises:
        enterprise.districts.set(districts[:2])
    return enterprises


@pytest.fixture
def network_products(categories, enterprise_networks, network_enterprises):
    products = []
    for category in categories:
        products.extend(
            ProductFactory.create_batch(
                2, category=category, enterprise_network=enterprise_networks[0]
            )
        )
    for index, enterprise in enumerate(network_enterprises):
        ProductPriceFactory.create(enterprise=enterprise, product=products[index])
    return products

