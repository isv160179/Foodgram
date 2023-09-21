import re

from django.conf import settings
from django.core.exceptions import ValidationError

SYMBOLS_WRONG = 'Использовать символ(ы): {} в составе логина запрещено!'


def username_validator(value):
    """Проверка на использование запрещенных символов."""
    denied_symbols = re.sub(
        settings.ALLOWED_SYMBOLS_FOR_LOGIN, '', value
    )
    if denied_symbols:
        raise ValidationError(
            SYMBOLS_WRONG.format(''.join(set(denied_symbols)))
        )
    return value
