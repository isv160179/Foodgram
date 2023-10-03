from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse

import recipes.constants as const

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=const.TAG_NAME_MAX_LENGTH,
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=const.TAG_COLOR_MAX_LENGTH,
        validators=(
            RegexValidator(
                regex=const.ALLOWED_SYMBOLS_FOR_COLOR,
                message=const.COLOR_SYMBOLS_ERROR,
            ),
        ),
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=const.TAG_SLUG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return const.TAG_TEMPLATE.format(
            self.name,
            self.color
        )

    def get_absolute_url(self):
        return reverse('tag', args=(self.slug,))


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование ингредиента',
        max_length=const.INGREDIENT_MAX_LENGTH,
    )

    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=const.MEASUREMENT_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return const.INGREDIENT_TEMPLATE.format(
            self.name,
            self.measurement_unit,
        )


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        through='RecipeIngredient',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        related_name='recipes'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipes/',
        blank=False,
        null=False,
    )
    name = models.CharField(
        'Наименование рецепта',
        max_length=const.RECIPE_MAX_LENGTH,
    )
    text = models.TextField('Описание рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                const.COOKING_TIME_MIN,
                message=const.COOKING_ERROR.format(const.COOKING_TIME_MIN),
            ),
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pk',)

    def __str__(self):
        return const.RECIPE_TEMPLATE.format(self.name)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='recipe_ingredient',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                const.INGREDIENT_MIN_VALUE,
                message=const.INGREDIENT_ERROR.format(
                    const.INGREDIENT_MIN_VALUE
                )
            ),
        ),
    )

    class Meta:
        verbose_name = 'Рецепт с ингредиентом'
        verbose_name_plural = 'Рецепты с ингредиентами'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_ingredient',
            ),
        )

    def __str__(self):
        return const.INGREDIENT_IN_RECIPE_TEMPLATE.format(
            self.ingredient.name,
            self.amount,
            self.ingredient.measurement_unit
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorite',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='favorite',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorites',
            ),
        )

    def __str__(self):
        return const.FAVORITE_TEMPLATE.format(
            self.recipe,
            self.user,
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Список рецептов',
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_shopping_cart'
            ),
        )

    def __str__(self):
        return const.SHOPING_CART_TEMPLATE.format(self.user)
