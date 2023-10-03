import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Создание суперпользователя в безинтерактивном режиме."

    def add_arguments(self, parser):
        parser.add_argument('--username', help='Логин администратора')
        parser.add_argument('--email', help='E-mail администратора')
        parser.add_argument('--password', help='Пароль администратора')
        parser.add_argument('--first_name', help='Имя администратора')
        parser.add_argument('--last_name', help='Фамилия администратора')
        parser.add_argument(
            '--no-input',
            help='Опция для чтения данных из файла окружения',
            action='store_true'
        )

    def handle(self, *args, **options):
        if options['no_input']:
            options['username'] = os.environ['SUPERUSER_USERNAME']
            options['email'] = os.environ['SUPERUSER_EMAIL']
            options['password'] = os.environ['SUPERUSER_PASSWORD']
            options['first_name'] = os.environ['SUPERUSER_FIRSTNAME']
            options['last_name'] = os.environ['SUPERUSER_LASTNAME']

        if not User.objects.filter(
                username=options['username'],
                email=options['email']
        ).exists():
            User.objects.create_superuser(
                username=options['username'],
                email=options['email'],
                password=options['password'],
                first_name=options['first_name'],
                last_name=options['last_name'],
                role=User.UserRole.ADMIN
            )
