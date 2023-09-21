from django.contrib import admin
from django.utils.safestring import mark_safe

from recipes.models import Tag, Ingredient, IngredientInRecipie, Recipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color',)
    search_fields = ('name', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


@admin.register(IngredientInRecipie)
class IngredientInRecipieAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'ingredient', 'amount', 'get_measurement_unit',
        'get_recipes_count',
    )

    @admin.display(description='Единица измерения')
    def get_measurement_unit(self, obj):
        try:
            return obj.ingredient.measurement_unit
        except IngredientInRecipie.ingredient.RelatedObjectDoesNotExist:
            return '----'

    @admin.display(description='Количество рецептов')
    def get_recipes_count(self, obj):
        return obj.recipes.count()


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'get_html_image', 'added_in_favorites')

    @admin.display(description='Изображение рецепта')
    def get_html_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=50>')

    @admin.display(description='Рецептов в избранном')
    def added_in_favorites(self, obj):
        return obj.favorites.count()
