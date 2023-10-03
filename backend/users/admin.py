from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model

from users.models import Subscribe

User = get_user_model()


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_blocked',
        'role',
    )
    list_filter = (
        'email', 'username', 'is_blocked', 'role',
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'username', 'first_name', 'last_name',
        )}),
        ('Атрибуты пользователя', {'fields': ('is_blocked', 'role',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'password1',
                'password2', 'is_blocked', 'role',
            )
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    ordering = ('id', 'email', 'username',)


@admin.register(Subscribe)
class SubscribeAdmin(ModelAdmin):
    list_display = ('user', 'author',)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
