from rest_framework.exceptions import ValidationError

from recipes.constants import FIELD_IS_REQUREST


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
