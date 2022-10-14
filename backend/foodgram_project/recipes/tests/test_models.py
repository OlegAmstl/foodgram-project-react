import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from ingredients.models import Ingredient, MeasurementUnit
from recipes.models import (Recipe, RecipeIngredientAmount, RecipeTag,
                            UserFavoriteRecipe, UserShoppingCart)
from tags.models import Tag
from users.models import User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RecipeModelsTest(TestCase):
    '''Тестируем модель Recipe.'''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.USER_DATA = {
            'first_name': 'Тест',
            'last_name': 'Тестович',
            'email': 'test@test_domain.info',
            'username': 'usertest',
            'password': 'test_123',
        }

        cls.user = User.objects.create_user(**cls.USER_DATA)
        cls.tag = Tag.objects.create(
            name='Tag1',
            slug='Tag_1',
            color='#111111',
        )
        cls.m_u = MeasurementUnit.objects.create(name='Mu1')
        cls.ingred = Ingredient.objects.create(
            name='ingred_1', measurement_unit=cls.m_u)
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.recipe = Recipe.objects.create(
            author=cls.user, name='Тест Рецепт', text='Много текста',
            cooking_time=42, image=cls.uploaded
        )
        cls.recipe_tag = RecipeTag.objects.create(
            recipe=cls.recipe, tag=cls.tag
        )
        cls.recipe_ingredient_amount = RecipeIngredientAmount.objects.create(
            recipe=cls.recipe, ingredient=cls.ingred, amount=37
        )
        cls.favorite_recipe = UserFavoriteRecipe.objects.create(
            user=cls.user, recipe=cls.recipe
        )
        cls.shop_recipe = UserShoppingCart.objects.create(
            user=cls.user, recipe=cls.recipe
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_recipes_models_recipe_have_correct_verbose_name(self):
        field_verboses = {
            'author': 'Автор',
            'name': 'Название',
            'text': 'Описание',
            'cooking_time': 'Время приготовления (в минутах)',
            'tags': 'Тег',
            'ingredients': 'Список ингредиентов'
        }
        recipe = RecipeModelsTest.recipe
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    recipe._meta.get_field(field).verbose_name,
                    expected_value, (
                        'Тест не пройден, '
                        f'{recipe._meta.get_field(field).verbose_name} '
                        f'вместо {expected_value}'
                    )
                )

    def test_recipes_models_recipe_have_correct_help_text(self):
        field_help_text = {
            'author': 'Автор',
            'name': 'Название',
            'text': 'Описание',
            'cooking_time': 'Время приготовления (в минутах)',
            'tags': 'Тег',
            'ingredients': 'Список ингредиентов'
        }
        recipe = RecipeModelsTest.recipe
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    recipe._meta.get_field(field).help_text,
                    expected_value,
                    (
                        'Тест не пройден, '
                        f'{recipe._meta.get_field(field).help_text} '
                        f'вместо {expected_value}'
                    )
                )

    def test_recipes_models_recipe_have_correct_max_length(self):
        field_max_length = {
            'name': 200,
        }
        recipe = RecipeModelsTest.recipe
        for field, expected_value in field_max_length.items():
            with self.subTest(field=field):
                self.assertEqual(
                    recipe._meta.get_field(field).max_length,
                    expected_value,
                    (
                        'Тест не пройден, '
                        f'{recipe._meta.get_field(field).max_length} '
                        f'вместо {expected_value}'
                    )
                )

    def test_recipes_models_recipe_tags_have_correct_fields(self):
        recipe_tag = RecipeModelsTest.recipe_tag

        field_verboses = {
            'recipe': 'Рецепт',
            'tag': 'Тег',
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    recipe_tag._meta.get_field(field).verbose_name,
                    expected_value, (
                        'Некореектный verbose_name, '
                        f'{recipe_tag._meta.get_field(field).verbose_name} '
                        f'вместо {expected_value}'
                    )
                )

        field_help_text = {
            'recipe': 'Рецепт',
            'tag': 'Тег',
        }

        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    recipe_tag._meta.get_field(field).help_text,
                    expected_value,
                    (
                        'Некореектный help_text, '
                        f'{recipe_tag._meta.get_field(field).help_text} '
                        f'вместо {expected_value}'
                    )
                )

    def test_models_recipe_ingredients_amount_have_correct_fields(self):
        recipe_ingred = RecipeModelsTest.recipe_ingredient_amount

        field_verboses = {
            'recipe': 'Рецепт',
            'ingredient': 'Ингридиент',
            'amount': 'Количество',
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    recipe_ingred._meta.get_field(field).verbose_name,
                    expected_value, (
                        'Некореектный verbose_name, '
                        f'{recipe_ingred._meta.get_field(field).verbose_name} '
                        f'вместо {expected_value}'
                    )
                )

        field_help_text = {
            'recipe': 'Рецепт',
            'ingredient': 'Ингридиент',
            'amount': 'Количество',
        }

        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    recipe_ingred._meta.get_field(field).help_text,
                    expected_value,
                    (
                        'Некореектный help_text, '
                        f'{recipe_ingred._meta.get_field(field).help_text} '
                        f'вместо {expected_value}'
                    )
                )

    def test_recipes_models_user_favorite_recipe_have_correct_fields(self):
        favor_recipe = RecipeModelsTest.favorite_recipe

        field_verboses = {
            'recipe': 'Рецепт',
            'user': 'Пользователь',
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    favor_recipe._meta.get_field(field).verbose_name,
                    expected_value, (
                        'Некореектный verbose_name, '
                        f'{favor_recipe._meta.get_field(field).verbose_name} '
                        f'вместо {expected_value}'
                    )
                )

        field_help_text = {
            'recipe': 'Рецепт',
            'user': 'Пользователь',
        }

        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    favor_recipe._meta.get_field(field).help_text,
                    expected_value,
                    (
                        'Некореектный help_text, '
                        f'{favor_recipe._meta.get_field(field).help_text} '
                        f'вместо {expected_value}'
                    )
                )

    def test_recipes_models_user_shopping_cart_have_correct_fields(self):
        shop_recipe = RecipeModelsTest.shop_recipe

        field_verboses = {
            'recipe': 'Рецепт',
            'user': 'Пользователь',
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    shop_recipe._meta.get_field(field).verbose_name,
                    expected_value, (
                        'Некореектный verbose_name, '
                        f'{shop_recipe._meta.get_field(field).verbose_name} '
                        f'вместо {expected_value}'
                    )
                )

        field_help_text = {
            'recipe': 'Рецепт',
            'user': 'Пользователь',
        }

        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    shop_recipe._meta.get_field(field).help_text,
                    expected_value,
                    (
                        'Некореектный help_text, '
                        f'{shop_recipe._meta.get_field(field).help_text} '
                        f'вместо {expected_value}'
                    )
                )
