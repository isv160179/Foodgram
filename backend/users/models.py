from django.contrib.auth.models import AbstractUser
from django.db import models

import users.constants as const
from users.validators import username_validator


class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = 'Admin'
        USER = 'User'

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=const.EMAIL_MAX_LENGTH,
        unique=True
    )
    username = models.CharField(
        'Логин',
        max_length=const.USERNAME_MAX_LENGTH,
        unique=True,
        validators=(username_validator,)
    )
    first_name = models.CharField(
        'Имя',
        max_length=const.FIRST_NAME_MAX_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=const.LAST_NAME_MAX_LENGTH
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=max(len(choice) for choice, _ in UserRole.choices),
        choices=UserRole.choices, default=UserRole.USER, )
    is_blocked = models.BooleanField(
        'Заблокирован',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN or self.is_staff

    class Meta:
        ordering = ('last_name', 'first_name', 'username')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return const.USER_TEMPLATE.format(
            self.first_name,
            self.last_name
        )


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='subscribing',
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscribe',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='check_self_subscribing',
            ),
        )

    def __str__(self):
        return const.SUBSCRIBE_TEMPLATE.format(self.user, self.author)
