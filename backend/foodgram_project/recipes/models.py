from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from foodgram_project.settings import PROJECT_SETTINGS
from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    '''Класс для описания рецептов.'''

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Автор',
        related_name='recipes',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Название',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Время приготовления (в минутах)',
        validators=(
            MinValueValidator(
                limit_value=PROJECT_SETTINGS.get('recipes_min_cooking_time', 1)
            ),
        )
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Тег',
        help_text='Тег'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        verbose_name='Список ингредиентов',
        help_text='Список ингредиентов'
    )
    favorite = ManyToManyField(
        User,
        verbose_name='Понравившиеся рецепты',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'Рецепт: {self.name}'


class RecipeTag(models.Model):
    '''Класс для описания тега.'''

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Рецепт',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег',
        help_text='Тег',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unigue_tag_for_recipe'
            ),
        )

    def __str__(self) -> str:
        return f'{self.recipe.name}, {self.tag.name}'


class RecipeIngredientAmount(models.Model):
    '''Класс для количества ингредиентов.'''

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Рецепт',
        db_index=True,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        help_text='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Количество',
        validators=(
            MinValueValidator(
                limit_value=PROJECT_SETTINGS.get('ingredient_min_amount', 1)
            ),
        )
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unigue_ingredient_for_recipe'
            ),
        )

    def __str__(self) -> str:
        return f'{self.recipe.name}, {self.ingredient.name}'


class UserFavoriteRecipe(models.Model):
    '''Класс для избранных рецептов.'''

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='favorite_recipes',
        verbose_name='Пользователь',
        help_text='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='in_favorite',
        verbose_name='Рецепт',
        help_text='Рецепт'
    )

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unigue_recipe_user_favorite'
            ),
        )

    def __str__(self) -> str:
        return f'{self.user.username}, {self.recipe.name}'


class UserShoppingCart(models.Model):
    '''Класс для списка покупок.'''

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='shopping_recipes',
        verbose_name='Пользователь',
        help_text='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='in_shopping',
        verbose_name='Рецепт',
        help_text='Рецепт'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unigue_recipe_user_shoping'
            ),
        )

    def __str__(self) -> str:
        return f'{self.user.username}, {self.recipe.name}'
