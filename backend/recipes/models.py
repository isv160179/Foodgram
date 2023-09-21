from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from recipes.constants import (
    TAG_NAME_MAX_LENGTH,
    TAG_COLOR_MAX_LENGTH,
    ALLOWED_SYMBOLS_FOR_COLOR,
    COLOR_SYMBOLS_ERROR,
    TAG_SLUG_MAX_LENGTH,
    TAG_TEMPLATE, INGREDIENT_MAX_LENGTH, MEASUREMENT_MAX_LENGTH,
    INGREDIENT_TEMPLATE, INGREDIENT_MIN_VALUE, INGREDIENT_ERROR,
    INGREDIENT_IN_RECIPIE_TEMPLATE, RECIPE_MAX_LENGTH, COOKING_TIME_MIN,
    COOKING_ERROR, RECIPE_TEMPLATE,
)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=TAG_NAME_MAX_LENGTH,
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=TAG_COLOR_MAX_LENGTH,
        validators=(
            RegexValidator(
                regex=ALLOWED_SYMBOLS_FOR_COLOR,
                message=COLOR_SYMBOLS_ERROR,
            ),
        ),
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=TAG_SLUG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return TAG_TEMPLATE.format(
            self.name,
            self.color
        )

    # def get_absolute_url(self):
    #     return reverse('tag', args=(self.slug,))


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование ингредиента',
        max_length=INGREDIENT_MAX_LENGTH,
    )

    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MEASUREMENT_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return INGREDIENT_TEMPLATE.format(
            self.name,
            self.measurement_unit,
        )


class IngredientInRecipie(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                INGREDIENT_MIN_VALUE,
                message=INGREDIENT_ERROR.format(INGREDIENT_MIN_VALUE)
            ),
        ),
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            UniqueConstraint(
                fields=('ingredient', 'amount',),
                name='unique_ingredient',
            ),
        )

    def __str__(self):
        return INGREDIENT_IN_RECIPIE_TEMPLATE.format(
            self.ingredient.name,
            self.amount,
            self.ingredient.measurement_unit
        )


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        IngredientInRecipie,
        verbose_name='Список ингредиентов',
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
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipes/images/',
    )
    name = models.CharField(
        'Наименование рецепта',
        max_length=RECIPE_MAX_LENGTH,
    ),
    text = models.TextField('Описание')

    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                COOKING_TIME_MIN,
                message=COOKING_ERROR.format(COOKING_TIME_MIN),
            ),
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id', )

    def __str__(self):
        return RECIPE_TEMPLATE.format(
            self.name,
            self.author
        )

    # def get_absoulute_url(self):
    #     return reverse('recipe', args=(self.pk,))
