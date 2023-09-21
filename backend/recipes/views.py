from recipes.mixins import RetriveListModelMixin
from recipes.models import Tag
from recipes.serializers import TagSerializer


class TagViewSet(RetriveListModelMixin):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)
