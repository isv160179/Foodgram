TAG_NAME_MAX_LENGTH = 200
TAG_SLUG_MAX_LENGTH = 200
TAG_COLOR_MAX_LENGTH = 7
INGREDIENT_MAX_LENGTH = 200
MEASUREMENT_MAX_LENGTH = 200
RECIPE_MAX_LENGTH = 200
INGREDIENT_MIN_VALUE = 1
COOKING_TIME_MIN = 1

ALLOWED_SYMBOLS_FOR_COLOR = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

COLOR_SYMBOLS_ERROR = 'Не верный формат кода цвета в шестнадцатеричном виде.'
INGREDIENT_ERROR = 'Количество ингредиента не может быть меньше {}.'
COOKING_ERROR = 'Время приготовления рецепта не может быть меньше {}.'

TAG_TEMPLATE = 'Тег {} соответствует цвету {}.'
INGREDIENT_TEMPLATE = '{} - {}'
RECIPE_TEMPLATE = 'Рецепт {}.'
INGREDIENT_IN_RECIPE_TEMPLATE = 'Ингредиент {} в количестве {} {}.'
FAVORITE_TEMPLATE = 'Рецепт {} в избранном пользователя {}.'
SHOPING_CART_TEMPLATE = 'Список покупок пользователя {}.'
SHOPING_CART = 'Ингредиент {} в количестве {} {}.'
SHOPING_CART_FILE_NAME = 'shopping_cart.txt'

RECIPE_ALREADY_EXIST = 'Рецепт ранее уже был добавлен.'
RECIPE_NOT_EXIST = 'Рецепта не существует.'
RECIPE_SUCSESS_DELETE = 'Рецепт успешно удален.'

INGREDIENT_NULL_ERROR = 'У рецепта должен быть хотя бы один ингредиент.'
TAG_NULL_ERROR = 'У рецепта должен быть хотя бы один тег.'
INGREDIENT_UNIQUE_ERROR = 'Ингредиенты одного рецепта должны быть уникальные.'
TAG_UNIQUE_ERROR = 'Теги одного рецепта должны быть уникальные.'

FIELD_IS_NONE_ERROR = 'Значение не может быть пустым.'
FIELD_IS_REQUREST = 'Обязательное поле.'

PULL_SUCCSESS = 'Данные для таблицы :{}, ЗАГРУЖЕНЫ!'
