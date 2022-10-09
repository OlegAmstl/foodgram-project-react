from recipes.models import AmountIngredient
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


def amount_ingredients_set(recipe, ingredients):
    for ingredient in ingredients:
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=ingredient['ingredient'],
            amount=ingredient['amount']
        )


def check_value_validate(value, klass=None):
    """Проверяет корректность переданного значения."""
    if not str(value).isdecimal():
        raise ValidationError(
            f'{value} должно содержать цифру'
        )
    if klass:
        obj = klass.objects.filter(id=value)
        if not obj:
            raise ValidationError(
                f'{value} не существует'
            )
        return obj[0]


class AddDelViewMixin:
    """Добавляет во viewset новые методы."""

    add_serializer = None

    def add_dell_obj(self, obj_id, manager):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        managers = {
            'subscribe': user.subscribe,
            'favorite': user.favorites,
            'shopping_list': user.shopping_list
        }
        manager = managers[manager]
        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.add_serializer(
            obj, context={'request': self.request}
        )
        obj_exist = manager.filter(id=obj_id).exists()

        if (self.request.method in ('GET', 'POST',)) and not obj_exist:
            manager.add(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if (self.request.method in ('DELETE',)) and obj_exist:
            manager.remove(obj)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
