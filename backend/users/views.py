from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import users.constants as const
from foodgram.pagination import CustomPagination
from users.models import Subscribe, User
from users.serializers import SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    """
    Кастомный вьюсет пользователя для работы с подписками.
    """
    pagination_class = CustomPagination
    lookup_url_kwarg = 'user_id'

    def get_permissions(self):
        """
        Ограничивает доступ к эндпоинту me неавторизованным пользователям.
        """
        if self.action == 'me':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def get_subscribe_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return SubscribeSerializer(*args, **kwargs)

    def create_subscribe(self, request, author):
        """
        Метод создания подписки на автора.
        """
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
        """
        Метод удаления подписки.
        """
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
        """
        Action метод показа всех подписок пользователя.
        """
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
        """
        Action метод управления подпиской.
        """
        author = get_object_or_404(User, pk=user_id)
        if request.method == 'POST':
            return self.create_subscribe(request, author)
        return self.delete_subscribe(request, author)

    @action(
        methods=('POST',),
        detail=False
    )
    def set_password(self, request, *args, **kwargs):
        """
        Кастомный Action метод изменения пароля.
        """
        super().set_password(request, *args, **kwargs)
        return Response(
            {const.PASSWORD_CHANGE_SUCCESS},
            status=status.HTTP_204_NO_CONTENT
        )


class CustomTokenCreateView(TokenCreateView):
    """
    Кастомный вьюсет создания токена.
    """

    def _action(self, serializer):
        if serializer.user.is_blocked:
            return Response(
                {'errors': const.USER_IS_BLOCKED},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            data=super()._action(serializer).data,
            status=status.HTTP_201_CREATED)


class CustomTokenDestroyView(TokenDestroyView):
    """
    Кастомный вьюсет удаления токена.
    """

    def post(self, request):
        super().post(request)
        return Response(
            {const.DESTROY_TOKEN_SUCCESS},
            status=status.HTTP_204_NO_CONTENT
        )
