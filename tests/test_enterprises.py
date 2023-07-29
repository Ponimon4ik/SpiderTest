import pytest


class TestEnterprisesAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_enterprises_not_authenticated(self, client, districts):
        district = districts[0]
        response = client.get(f'/api/v1/districts/{district.id}/organizations/')
        assert response.status_code != 404, (
            'Страница `/api/v1/districts/{district.id}/organizations/` '
            f'не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/v1/districts/{district.id}/organizations/` '
            'без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_enterprise_not_authenticated(self, client, districts, network_products):
        district = districts[0]
        response = client.get(
            f'/api/v1/districts/{district.id}/organizations/{district.enterprises.all()[0].id}/')
        assert response.status_code != 404, (
            'Страница `/api/v1/districts/{district.id}/organizations/{enterprise_id}/`'
            ' не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `'
            '/api/v1/districts/{district.id}/organizations/{enterprise_id}/` '
            'без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_enterprises_authenticated(self, user_client, districts, network_products):
        district = districts[0]
        response = user_client.get(f'/api/v1/districts/{district.id}/organizations/')
        assert response.status_code != 404, (
            'Страница `/api/v1/districts/{district.id}/organizations/` '
            f'не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/districts/{district.id}/organizations/` '
            'с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
        enterprises = [(item['name'], item['enterprise_network']) for item in response_data]
        for name, enterprise_network in enterprises:
            assert (
                name in [str(item[0]) for item in district.enterprises.all().values_list('name')]
                and enterprise_network in [
                    str(item[0]) for item in
                    district.enterprises.all().values_list('enterprise_network__name')
                ]
            ), (
                'Проверьте, что при GET запросе `/api/v1/districts/{district.id}/organizations/`'
                'возвращается правильные организации из БД'
            )

    @pytest.mark.django_db(transaction=True)
    def test_04_enterprise_authenticated(self, user_client, districts, network_products):
        district = districts[0]
        enterprise = district.enterprises.all()[0]
        response = user_client.get(
            f'/api/v1/districts/{district.id}/organizations/{enterprise.id}/')
        assert response.status_code != 404, (
            'Страница `/api/v1/districts/{district.id}/organizations/{enterprise_id}/` '
            f'не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 200, (
            'Проверьте, что при GET запросе '
            '`/api/v1/districts/{district.id}/organizations/{enterprise_id}/` '
            'с токеном авторизации возвращается статус 200'
        )

        response_data = response.json()
        assert (
            response_data['id'] == enterprise.id
            and response_data['name'] == enterprise.name
            and response_data['enterprise_network'] == enterprise.enterprise_network.name
            and response_data['districts'] == [
                item[0] for item in enterprise.districts.all().values_list('name')
            ]
        ), (
            'Проверьте что при запросе '
            '/api/v1/districts/{district.id}/organizations/{enterprise_id}/'
            'возвращается правильная организация из БД.'
        )
        products = [item['name'] for item in response_data['products']]
        assert products == [
            item[0] for item in enterprise.products.all().values_list('name')
        ], (
            'Проверьте что при запросе '
            '/api/v1/districts/{district.id}/organizations/{enterprise_id}/'
            'возвращаются правильные продукты для организации.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_05_post_enterprise(self, user_client, districts):
        district = districts[0]
        response = user_client.post(f'/api/v1/districts/{district.id}/organizations/')
        assert response.status_code == 405, (
            'Проверьте что post запрос ограничен для '
            '`/api/v1/districts/{district.id}/organizations/` '
        )
