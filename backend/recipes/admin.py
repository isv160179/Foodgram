from django.contrib import admin
from django.utils.safestring import mark_safe

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
        'get_measurement_unit'
    )

    @admin.display(description='Единица измерения')
    def get_measurement_unit(self, obj):
        try:
            return obj.ingredient.measurement_unit
        except RecipeIngredient.ingredient.RelatedObjectDoesNotExist:
            return '----'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'get_tags',
        'get_html_image',
        'count_in_favorites'
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)

    @admin.display(description='Теги рецепта')
    def get_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    @admin.display(description='Изображение рецепта')
    def get_html_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=50>')
        return '---'

    @admin.display(description='Количество рецептов в избранном')
    def count_in_favorites(self, obj):
        return obj.favorite.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
