import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из CSV в Базу данных SQLite'

    def handle(self, *args, **kwargs):
        self.stdout.write("###   НАЧИНАЮ!   ###")
        if Ingredient.objects.exists():
            print("Данные уже загружены!")
            return
        with open("data/ingredients.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=',')
            header = ['name', 'measurement_unit']
            try:
                for row in reader:
                    object_dict = {
                        key: value for key, value in zip(header, row)
                    }
                    Ingredient.objects.create(**object_dict)
            except ValueError as error:
                self.stdout.write("Ошибка :{}.".format(error))
            except TypeError as error:
                self.stdout.write("Ошибка :{}.".format(error))
        self.stdout.write('Данные модели ЗАГРУЖЕНЫ!')
        self.stdout.write('###  Готово !!!  ###')
