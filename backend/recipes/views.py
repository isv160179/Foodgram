from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import recipes.constants as const
from foodgram.pagination import CustomPagination
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from recipes.permissions import IsAdminOrAuthorOrReadOnly
from recipes.serializers import (FavoriteSerializer, IngredientSerializer,
                                 RecipeWriteSerializer, ShoppingCartSerializer,
                                 TagSerializer)


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
