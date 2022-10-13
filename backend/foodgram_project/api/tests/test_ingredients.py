from ingredients.models import Ingredient, MeasurementUnit
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class IngredientsTests(APITestCase):
    '''Тестируем /api/ingredients/.'''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mu_1 = MeasurementUnit.objects.create(id=1, name='mu_1')
        cls.mu_2 = MeasurementUnit.objects.create(id=2, name='mu_2')

        cls.ing_1 = Ingredient.objects.create(
            id=1, name='ing_1', measurement_unit=cls.mu_1)
        cls.ing_1 = Ingredient.objects.create(
            id=2, name='ing_2', measurement_unit=cls.mu_2)
        cls.ing_1 = Ingredient.objects.create(
            id=3, name='in_3g', measurement_unit=cls.mu_1)
        cls.ing_1 = Ingredient.objects.create(
            id=4, name='4_ing', measurement_unit=cls.mu_2)
        cls.ing_1 = Ingredient.objects.create(
            id=5, name='5_ing', measurement_unit=cls.mu_1)

        cls.base_url = '/api/ingredients/'

    def setUp(self):
        self.client = APIClient()

    def test_api_ingredients_01_url_list(self):
        url = IngredientsTests.base_url
        resp = self.client.get(url)
        self.assertEqual(
            resp.status_code, status.HTTP_200_OK,
        )

    def test_api_ingredients_02_url_retrieve(self):
        url = IngredientsTests.base_url + '1/'
        resp = self.client.get(url)
        self.assertEqual(
            resp.status_code, status.HTTP_200_OK,
        )

    def test_api_ingredients_03_url_retrieve_not_exist(self):
        url = IngredientsTests.base_url + '6/'
        resp = self.client.get(url)
        self.assertEqual(
            resp.status_code, status.HTTP_404_NOT_FOUND,
        )

    def test_api_ingredients_04_retrieve_correct_fields(self):
        url = IngredientsTests.base_url + '2/'
        ingred = Ingredient.objects.get(id=2)
        resp = self.client.get(url)
        try:
            resp_data = resp.json()
        except Exception as err:
            self.assertTrue(
                True,
                msg=f'responce data is not json: {err}'
            )
        fields_name = {
            'id': 2,
            'name': ingred.name,
            'measurement_unit': ingred.measurement_unit.name,
        }
        self.assertEqual(
            len(resp_data), len(fields_name),
            'Число полей в ответе не соответствует ожиданиям'
        )
        for field, value in fields_name.items():
            with self.subTest(field=field):
                self.assertEqual(
                    resp_data[field],
                    value,
                    f'Поле {field} не верное значение'
                )

    def test_api_ingredients_05_list_correct(self):
        url = IngredientsTests.base_url
        resp = self.client.get(url)
        try:
            resp_data = resp.json()
        except Exception as err:
            self.assertTrue(
                True,
                msg=f'responce data is not json: {err}'
            )
        self.assertIsInstance(resp_data, list, 'В ответе не list')
        self.assertEqual(
            len(resp_data), 5, 'В ответе не то число элементов списка'
        )
        for ingred_data in resp_data:
            with self.subTest(ingred_data=ingred_data):
                self.assertIsInstance(
                    ingred_data, dict, 'в ответе не список словарей'
                )
                self.assertIsNotNone(
                    ingred_data.get('id', None),
                    'В словаре нет ключа id'
                )
                id = ingred_data.get('id')
                ingred = Ingredient.objects.get(id=id)
                fields_name = {
                    'name': ingred.name,
                    'measurement_unit': ingred.measurement_unit.name,
                }
                self.assertEqual(
                    len(ingred_data), len(fields_name) + 1,
                    'Число ключей в ответе не соответствует ожидаемым'
                )
                for field_name, value in fields_name.items():
                    self.assertEqual(
                        ingred_data[field_name], value
                    )

    def test_api_ingredients_06_list_correct_with_filter_name(self):
        url = IngredientsTests.base_url + '?name=ing'
        resp = self.client.get(url)
        try:
            resp_data = resp.json()
        except Exception as err:
            self.assertTrue(
                True,
                msg=f'responce data is not json: {err}'
            )
        self.assertIsInstance(resp_data, list, 'В ответе не list')
        self.assertEqual(
            len(resp_data), 2, 'В ответе не то число элементов списка'
        )
        for ingred_data in resp_data:
            with self.subTest(ingred_data=ingred_data):
                self.assertIsInstance(
                    ingred_data, dict, 'в ответе не список словарей'
                )
                self.assertIsNotNone(
                    ingred_data.get('id', None),
                    'В словаре нет ключа id'
                )
                id = ingred_data.get('id')
                ingred = Ingredient.objects.get(id=id)
                fields_name = {
                    'name': ingred.name,
                    'measurement_unit': ingred.measurement_unit.name,
                }
                self.assertEqual(
                    len(ingred_data), len(fields_name) + 1,
                    'Число ключей в ответе не соответствует ожидаемым'
                )
                for field_name, value in fields_name.items():
                    self.assertEqual(
                        ingred_data[field_name], value
                    )
