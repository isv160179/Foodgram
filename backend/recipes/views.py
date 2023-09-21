from recipes.mixins import RetriveListModelMixin
from recipes.models import Tag, Ingredient
from recipes.serializers import TagSerializer, IngredientSerializer


class TagViewSet(RetriveListModelMixin):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)


class IngredientViewSet(RetriveListModelMixin):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    http_method_names = ('get',)