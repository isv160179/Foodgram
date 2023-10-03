from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import recipes.constants as const
from foodgram.serializers import RecipeSerializer
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from recipes.utils import Base64ImageField
from recipes.validators import not_exists_validate, null_unique_validator
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        read_only=True
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(
        read_only=True, many=True,
        source='recipe_ingredient'
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (
            obj.favorite.filter(user=user).exists()
            and user.is_authenticated
        )
        # if user.is_anonymous:
        #     return False
        # return obj.favorite.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (
            obj.shopping_cart.filter(user=user).exists()
            and user.is_authenticated
        )
        # if user.is_anonymous:
        #     return False
        # return obj.shopping_cart.filter(user=user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientWriteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'id',
            'tags',
            'image',
            'author',
            'name',
            'text',
            'cooking_time'
        )

    def validate_cooking_time(self, value):
        if value < const.COOKING_TIME_MIN:
            raise ValidationError(
                const.COOKING_ERROR_MIN.format(const.COOKING_TIME_MIN)
            )
        if value > const.COOKING_TIME_MAX:
            raise ValidationError(
                const.COOKING_ERROR_MAX.format(const.COOKING_TIME_MAX)
            )
        return value

    def validate_ingredients(self, value):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': const.FIELD_IS_NONE_ERROR}
            )
        null_unique_validator(
            value=value,
            message_dict={'null': const.INGREDIENT_NULL_ERROR,
                          'unique': const.INGREDIENT_UNIQUE_ERROR},
            item_list=[_['ingredient'] for _ in [_ for _ in value]]
        )
        return value

    def validate_tags(self, value):
        null_unique_validator(
            value=value,
            message_dict={'null': const.TAG_NULL_ERROR,
                          'unique': const.TAG_UNIQUE_ERROR}
        )
        return value

    def validate_image(self, value):
        if value is None:
            raise ValidationError(const.FIELD_IS_NONE_ERROR)
        return value

    def validate(self, data):
        for field in (
                'ingredients',
                'tags',
                'image',
                'name',
                'text',
                'cooking_time'
        ):
            not_exists_validate(field, data)
        return data

    def create_ingredients_in_recipe(self, recipe, ingredients):
        RecipeIngredient.objects.bulk_create(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient.get('ingredient'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self.context.get('request').user
        recipe = Recipe.objects.create(
            author=user,
            **validated_data
        )
        recipe.tags.set(tags)
        self.create_ingredients_in_recipe(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.set(tags)
        self.create_ingredients_in_recipe(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeReadSerializer(instance, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        user, recipe = data.get('user'), data.get('recipe')
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(
                {'errors': const.RECIPE_ALREADY_EXIST}
            )
        return data

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeSerializer(instance.recipe, context=context).data


class ShoppingCartSerializer(FavoriteSerializer):
    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart
