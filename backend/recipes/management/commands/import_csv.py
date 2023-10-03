import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipes.constants import PULL_SUCCSESS
from recipes.models import Ingredient, Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт данных из CSV в Базу данных Postgres'

    def handle(self, *args, **kwargs):
        patch_full = [
            {'file': 'ingredients.csv', 'obj': Ingredient},
            {'file': 'tags.csv', 'obj': Tag},
        ]
        for parameter in patch_full:
            patch = os.path.join(settings.BASE_DIR, 'data/', parameter['file'])
            with open(patch, 'r', encoding='utf-8') as f_csv:
                reader = csv.reader(f_csv, delimiter=',')
                header = next(reader)
                try:
                    for row in reader:
                        object_dict = {
                            key: value for key, value in zip(header, row)
                        }
                        parameter['obj'].objects.create(**object_dict)
                except (ValueError, TypeError) as error:
                    self.stdout.write('Ошибка :{}.'.format(error))
            self.stdout.write(PULL_SUCCSESS.format(parameter['file']))
