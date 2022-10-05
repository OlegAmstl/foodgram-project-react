from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from recipes.models import Tag, Ingredient


User = get_user_model()


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


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True,
                         read_only=True)

