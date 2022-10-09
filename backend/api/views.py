from django.shortcuts import render
from urllib.parse import unquote
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .pagination import FoodgramPaginator
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from .serializers import (SubscribeUsersSerializer, TagSerializer,
                          IngredientSerializer, RecipeSerializer,
                          SimpleRecipeSerializer)
from .utils import AddDelViewMixin
from .permisions import AdminOrReadOnly, AuthorStaffOrReadOnly
from recipes.models import Tag, Ingredient, Recipe, AmountIngredient

User = get_user_model()

CORRECT_SYMBOLS = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)
ACTION_METHODS = ['get', 'post', 'delete']


class MyUserViewSet(UserViewSet, AddDelViewMixin):
    """Работа с пользователями."""

    pagination_class = FoodgramPaginator
    add_serializer = SubscribeUsersSerializer

    @action(methods=ACTION_METHODS, detail=True)
    def subscribe(self, request, id):
        return self.add_dell_obj(id, 'subscribe')

    @action(methods=['get', ], detail=False)
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        authors = user.subscribe.all()
        pages = self.paginate_queryset(authors)
        serializer = SubscribeUsersSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    """Работа с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Работа с ингредиетами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)

    def get_queryset(self):
        title = self.request.query_params.get('title')
        queryset = self.queryset
        if title:
            if title[0] == '%':
                title = unquote(title)
            else:
                title = title.translate(CORRECT_SYMBOLS)
            title.lower()
            stw_queryset = list(queryset.filter(title__startswith=title))
            cnt_queryset = queryset.filter(title__contains=title)
            stw_queryset.extend(
                [i for i in cnt_queryset if i not in stw_queryset]
            )
            queryset = stw_queryset
        return queryset


class RecipeViewSet(ModelViewSet, AddDelViewMixin):
    """Работа с рецептами."""

    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    permission_classes = (AuthorStaffOrReadOnly,)
    pagination_class = FoodgramPaginator
    add_serializer = SimpleRecipeSerializer

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.query_params.getlist('tag')
        if tags:
            queryset = queryset.filter(tag__slug__in=tags).distinct()

        author = self.request.query_params('author')
        if author:
            queryset = queryset.filter(author=author)

        user = self.request.user
        if user.is_anonymous:
            return queryset

        is_in_shopping = self.request.query_params.get('is_shopping_list')
        if is_in_shopping in ('1', 'true',):
            queryset = queryset.filter(shopping_list=user.id)
        elif is_in_shopping in ('0', 'false',):
            queryset = queryset.exclude(shopping_list=user.id)

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited in ('1', 'true',):
            queryset = queryset.filter(favorites=user.id)
        if is_favorited in ('0', 'false',):
            queryset = queryset.exclude(favorites=user.id)

        return queryset

    @action(methods=ACTION_METHODS, detail=True)
    def favorite(self, request, pk):
        return self.add_dell_obj(pk, 'favorite')

    @action(methods=ACTION_METHODS, detail=True)
    def shopping_list(self, request, pk):
        return self.add_dell_obj(pk, 'shopping_list')
