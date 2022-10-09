from rest_framework.serializers import (ModelSerializer, ValidationError,
                                        SerializerMethodField)
from django.db.models import F
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Tag, Ingredient, Recipe, AmountIngredient
from .utils import amount_ingredients_set, check_value_validate


User = get_user_model()


class SubscribeUsersSerializer(ModelSerializer):
    """Сериализатор списка авторов на которых подписан."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = '__all__'

    def get_recipes_count(self, obj):
        """Выводит количество рецептов у автора."""
        return obj.recipes.count()


class UserSerializer(ModelSerializer):
    """Сериалайзер для модели User."""

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = 'is_subscribed'

    def get_is_subscribed(self, obj):
        """Проверка подписан ли данный юзер на просматриемого автора."""
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()

    def create(self, validated_data):
        """Создание нового пользователя."""
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(ModelSerializer):
    """Сериалайзер для тега."""

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__'


class IngredientSerializer(ModelSerializer):
    """Сериализатор для вывода ингридиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__'


class SimpleRecipeSerializer(ModelSerializer):
    """Сериализатор для модели Recipe."""
    class Meta:
        model = Recipe
        fields = 'id', 'title', 'image', 'cooking_time'
        read_only_fields = '__all__',


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(
        many=True,
        read_only=True
    )
    author = UserSerializer(
        read_only=True
    )
    ingredients = IngredientSerializer()
    is_favorited = SerializerMethodField()
    is_shopping_list = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'title',
            'author',
            'tag',
            'description',
            'cooking_time',
            'favorites',
            'image',
            'shopping_list',
            'ingredients'
        )
        read_only = (
            'favorites',
            'shopping_list'
        )

    def create(self, validated_data):
        """Создание рецепта."""
        tags = validated_data.pop('tag')
        ingredients = validated_data.pop('ingredients')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tag.set(tags)
        amount_ingredients_set(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        """Обновление рецепта."""
        tags = validated_data.get('tag')
        ingredients = validated_data.get('ingredients')
        recipe.image = validated_data.get(
            'image',
            recipe.image
        )
        recipe.title = validated_data.get(
            'title',
            recipe.title
        )
        recipe.description - validated_data.get(
            'description',
            recipe.description
        )
        recipe.cooking_time = validated_data.get(
            'cooking_time',
            recipe.cooking_time
        )

        if tags:
            recipe.tag.clear()
            recipe.tag.set(tags)
        if recipe.ingredients:
            recipe.ingredients.clear()
            amount_ingredients_set(recipe, ingredients)

        recipe.save()
        return recipe

    def get_ingredients(self, obj):
        """Получает список ингридиентов для рецепта."""
        ingredients = obj.ingredients.values(
            'id', 'title', 'unit', amount=F('recipe__amount')
        )
        return ingredients

    def get_is_in_shopping_list(self, obj):
        """Проверка - находится ли рецепт в списке  покупок."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_lists.filter(id=obj.id).exists()

    def get_is_favorited(self, obj):
        """Проверка - находится ли рецепт в избранном."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(id=obj.id).exists()

    def validate(self, data):
        """Проверка вводных данных при создании/редактировании рецепта."""
        title = str(self.initial_data.get('title')).strip()
        tags = self.initial_data.get('tag')
        ingredients = self.initial_data.get('ingredients')
        values_as_list = (tags, ingredients)

        for value in values_as_list:
            if not isinstance(value, list):
                raise ValidationError(
                    f'"{value}" должен быть в формате "[]"'
                )

        for tag in tags:
            check_value_validate(tag, Tag)

        valid_ingredients = []
        for ing in ingredients:
            ing_id = ing.get('id')
            ingredient = check_value_validate(ing_id, Ingredient)

            amount = ing.get('amount')
            check_value_validate(amount)

            valid_ingredients.append(
                {'ingredient': ingredient, 'amount': amount}
            )

        data['title'] = title.capitalize()
        data['tag'] = tags
        data['ingredients'] = valid_ingredients
        data['author'] = self.context.get('request').user
        return data


