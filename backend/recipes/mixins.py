from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet


class RetriveListModelMixin(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
):
    pass
