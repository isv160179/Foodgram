from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

import api.constants as const
from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAdminOrAuthorOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeWriteSerializer, ShoppingCartSerializer,
                             SubscribeSerializer, TagSerializer)
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import Subscribe

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination
    lookup_url_kwarg = 'user_id'

    def get_permissions(self):

        if self.action == 'me':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def get_subscribe_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return SubscribeSerializer(*args, **kwargs)

    def create_subscribe(self, request, author):

        if request.user == author:
            return Response(
                {'errors': const.SUBSCRIBE_ERROR},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            subscribe = Subscribe.objects.create(
                user=request.user,
                author=author,
            )
        except IntegrityError:
            return Response(
                {'errors': const.ALREADY_IS_SUBSCRIBE.format(author)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_subscribe_serializer(subscribe.author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_subscribe(self, request, author):

        try:
            Subscribe.objects.get(user=request.user, author=author).delete()
        except Subscribe.DoesNotExist:
            return Response(
                {'errors': const.SUBSCRIBE_NOT_EXIST.format(author)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'detail': const.UNSUBSCRIBE_SUCCESS.format(author)},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):

        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_subscribe_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_subscribe_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=('POST', 'DELETE',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, user_id=None):

        author = get_object_or_404(User, pk=user_id)
        if request.method == 'POST':
            return self.create_subscribe(request, author)
        return self.delete_subscribe(request, author)

    @action(
        methods=('POST',),
        detail=False
    )
    def set_password(self, request, *args, **kwargs):

        super().set_password(request, *args, **kwargs)
        return Response(
            {const.PASSWORD_CHANGE_SUCCESS},
            status=status.HTTP_204_NO_CONTENT
        )


class CustomTokenCreateView(TokenCreateView):

    def _action(self, serializer):
        if serializer.user.is_blocked:
            return Response(
                {'errors': const.USER_IS_BLOCKED},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            data=super()._action(serializer).data,
            status=status.HTTP_201_CREATED)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    pagination_class = CustomPagination

    def methods_for_actions(self, pk, serializer_class):
        user = self.request.user

        try:
            recipe = Recipe.objects.get(pk=pk)
            obj = serializer_class.Meta.model.objects.filter(
                user=user,
                recipe=recipe
            )
        except Recipe.DoesNotExist:
            obj = None
            Response({'errors': const.RECIPE_NOT_EXIST},
                     status=status.HTTP_400_BAD_REQUEST)

        if self.request.method == 'POST':
            serializer = serializer_class(
                data={'user': user.id, 'recipe': pk},
                context={'request': self.request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if obj is None:
                return Response({'errors': const.RECIPE_NOT_EXIST},
                                status=status.HTTP_400_BAD_REQUEST)
            obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True
    )
    def favorite(self, request, pk):
        return self.methods_for_actions(pk, FavoriteSerializer)

    @action(
        methods=['POST', 'DELETE'],
        detail=True
    )
    def shopping_cart(self, request, pk):
        return self.methods_for_actions(pk, ShoppingCartSerializer)

    @action(
        methods=['GET', ],
        detail=False
    )
    def download_shopping_cart(self, request):
        ingredient_list = (
            RecipeIngredient.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .order_by('ingredient__name')
            .annotate(total_summ=Sum('amount'))
        )
        result = const.SHOPING_CART_TEMPLATE.format(request.user) + '\n'
        result += '\n'.join(const.SHOPING_CART.format(
            ingredient['ingredient__name'],
            ingredient['total_summ'],
            ingredient['ingredient__measurement_unit']
        ) for ingredient in ingredient_list)

        response = HttpResponse(result, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename={const.SHOPING_CART_FILE_NAME}'
        )
        return response
