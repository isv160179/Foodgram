import re

from django.core.exceptions import ValidationError

import users.constants
from users.constants import SYMBOLS_WRONG


def username_validator(value):
    """Проверка на использование запрещенных символов."""
    denied_symbols = re.sub(
        users.constants.ALLOWED_SYMBOLS_FOR_LOGIN, '', value
    )
    if denied_symbols:
        raise ValidationError(
            SYMBOLS_WRONG.format(''.join(set(denied_symbols)))
        )
    return value
