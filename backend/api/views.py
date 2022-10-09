from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet

from .pagination import FoodgramPaginator
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from .serializers import SubscribeUsersSerializer, TagSerializer
from .utils import AddDelViewMixin
from .permisions import AdminOrReadOnly
from recipes.models import Tag, Ingredient, Recipe, AmountIngredient

User = get_user_model()


class MyUserViewSet(UserViewSet, AddDelViewMixin):
    """Работа с пользователями."""

    pagination_class = FoodgramPaginator
    add_serializer = SubscribeUsersSerializer

    @action(methods=['get', 'post', 'delete'], detail=True)
    def subscribe(self, request, id):
        return self.add_dell_obj(id, 'subscribe')

    @action(methods=['get',], detail=False)
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




