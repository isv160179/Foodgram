import re

from django.core.exceptions import ValidationError

from api.constants import (ALLOWED_SYMBOLS_FOR_LOGIN, FIELD_IS_REQUREST,
                           SYMBOLS_WRONG)


def username_validator(value):
    """Проверка на использование запрещенных символов."""
    denied_symbols = re.sub(
        ALLOWED_SYMBOLS_FOR_LOGIN, '', value
    )
    if denied_symbols:
        raise ValidationError(
            SYMBOLS_WRONG.format(''.join(set(denied_symbols)))
        )
    return value


def null_unique_validator(value, message_dict, item_list=None):
    if item_list:
        if len(set(item_list)) != len(item_list):
            raise ValidationError(message_dict['unique'])
    else:
        if len(set(value)) != len(value):
            raise ValidationError(message_dict['unique'])
    if len(value) == 0:
        raise ValidationError(message_dict['null'])


def not_exists_validate(field, data):
    if field not in data:
        raise ValidationError(
            {field: FIELD_IS_REQUREST}
        )
