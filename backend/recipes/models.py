from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """Тег для рецепта."""

    title: str = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название тега'
    )
    color: str = models.CharField(
        max_length=7,
        verbose_name='Цветовой HEX-код'
    )
    slug: str = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг тега',
        default='#00BFFF'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.title


class Ingredient(models.Model):
    """Ингредиент в составе рецепта."""

    title: str = models.CharField(
        max_length=50,
        verbose_name='Название ингредиента'
    )
    unit: str = models.CharField(
        max_length=15,
        verbose_name='Еденицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.title


class Recipe(models.Model):
    """Модель рецепта."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название рецепта'
    )
    author = models.ForeignKey(
        User,
        max_length=250,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    image = models.ImageField(
        upload_to='recipe_images/',
        verbose_name='Изображение блюда'
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Описание рецепта'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        default=0,
        verbose_name='Время готовки'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now=True
    )
    favorites = models.ManyToManyField(
        User,
        related_name='favorites',
        verbose_name='Избранные рецепты'
    )
    shopping_list = models.ManyToManyField(
        User,
        related_query_name='shopping_lists',
        verbose_name='Список покупок'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='recipes.AmountIngredient',
        verbose_name='Ингредиенты блюда'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class AmountIngredient(models.Model):
    """Количество ингредиента в блюде."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепты'
    )
    amount = models.PositiveIntegerField(
        default=0,
        verbose_name='В каком количестве'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингридиентов'

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredient}'
