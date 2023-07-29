import pytest


class TestProductAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_products_not_authenticated(self, client):
        response = client.get('/api/v1/products/')
        assert response.status_code != 404, (
            'Страница `/api/v1/products/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/v1/products/` '
            'без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_product_not_authenticated(self, client, network_products):
        product = network_products[0]
        response = client.get(f'/api/v1/products/{product.id}/')
        assert response.status_code != 404, (
            'Страница `/api/v1/products/{product.id}/` не найдена,'
            ' проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            f'Проверьте, что при GET запросе `/api/v1/products/{product.id}/` '
            'без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_products_authenticated(self, user_client):
        response = user_client.get('/api/v1/products/')

        assert response.status_code != 404, (
            'Страница `/api/v1/products/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 405, (
            'Проверьте, что при GET запросе `/api/v1/products/` '
            'возвращается статус 405 данный метод не разрешен'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_product_authenticated(self, user_client, network_products):
        product = network_products[0]
        response = user_client.get(f'/api/v1/products/{product.id}/')

        assert response.status_code != 404, (
            'Страница `/api/v1/products/{product.id}/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/products/{product.id}/` '
            'с токеном авторизации возвращается статус 200'
        )
        data = response.json()
        assert (
            data['id'] == product.id
            and data['name'] == product.name
            and data['category'] == product.category.name
            and data['enterprise_network'] == product.enterprise_network.name
            and data['description'] == product.description

        ), (
            'Проверьте, что при GET запросе `/api/v1/products/{product.id}/`'
            'возвращается правильный продукт из БД'
        )
        prices = [(item['enterprise'], item['price']) for item in data['prices']]
        for enterprise, price in prices:
            assert (
                enterprise in list(*product.products_prices.all().values_list('enterprise__name'))
                and price in [str(item) for item in list(*product.products_prices.all().values_list('price'))]
            ), (
                'Проверьте, что при GET запросе `/api/v1/products/{product.id}/`'
                'возвращаются правильные цены для продукта из БД'
            )

    @pytest.mark.django_db(transaction=True)
    def test_05_post_product(self, client, categories, enterprise_networks):
        enterprise_network = enterprise_networks[0]
        category = categories[0]
        data = {
            "name": "Какойто новый товар",
            "category": category.id,
            "enterprise_network": enterprise_network.id
        }
        response = client.post('/api/v1/products/', data=data)
        assert response.status_code == 401, (
            'Проверьте, что при POST запросе `/api/v1/products/` '
            'без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_05_post_product(self, user_client, categories, enterprise_networks):
        enterprise_network = enterprise_networks[0]
        category = categories[0]
        data = {
            "name": "Какойто новый товар",
            "category": category.id,
            "enterprise_network": enterprise_network.id
        }
        response = user_client.post('/api/v1/products/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/v1/products/` '
            'с токеном авторизации возвращается статус 201'
        )
        products = enterprise_network.products.filter(name=data['name'])
        assert len(products) == 1, (
            'Проверьте, что при POST запросе `/api/v1/products/` '
            'с токеном авторизации создается 1 запись в БД'
        )
