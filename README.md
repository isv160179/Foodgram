# Проект «Фудграм» 
Сайт, на котором пользователи могут публиковать рецепты, 
добавлять чужие рецепты в избранное и подписываться на 
публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». 
Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Главная страница:
- https://isv-foodgram.ddns.net
- http://158.160.69.96

Страница администрации сайта:
- https://isv-foodgram.ddns.net/admin/
- http://158.160.69.96/admin/

```
email: isv_admin@yandex.ru
password: admin
```
## Используемые технологии:
- Python 3.9
- Django==3.2
- djangorestframework==3.12.4
- djoser==2.2.0
- psycopg2-binary==2.9.7
- nodejs

## Локальный запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:isv160179/foodgram-project-react.git
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение, установить зависимости:

```
python3 -m venv venv 
source venv/scripts/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

Установите [docker compose](https://www.docker.com/) на свой компьютер.

Из корневой директории, где лежит файл docker-compose.yml,
запустите проект через docker-compose:

```
docker compose up --build -d
```

Выполнить миграции:

```
docker compose exec backend python manage.py migrate
```

Соберите статику и скопируйте ее:

```
docker compose exec backend python manage.py collectstatic
docker compose exec backend cp -r /app/collected_static/. /backend_static/
```

## .env

В корне проекта создайте файл .env и пропишите в него свои данные.

Пример:

```
SECRET_KEY='.....'
DB_ENGINE=django.db.backends.postgresql
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
DB_HOST=db
DB_PORT=5432
DEBUG=False
ALLOWED_HOSTS='127.0.0.1, localhost'
```

## Деплой на удаленном сервере с помощью Workflow

На удаленном сервере установите Docker Compose

```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin 

```
Скопируйте на сервер файл docker-compose.production.yml.
Создайте файл .env

Пример:

```
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY='.......'
DEBUG=False
ALLOWED_HOSTS='127.0.0.1, localhost, IP-адрес удаленного сервера, доменное имя удаленного сервера'
```

Для использования CI/CD: в репозитории GitHub Actions `Settings/Secrets/Actions` прописать Secrets - переменные окружения для доступа к сервисам:

```
DOCKER_USERNAME                # имя пользователя в DockerHub
DOCKER_PASSWORD                # пароль пользователя в DockerHub
HOST                           # ip_address сервера
USER                           # имя пользователя
SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa)
PASSPHRASE                     # кодовая фраза (пароль) для ssh-ключа
POSTGRES_USER                  # имя пользователя базы данных
POSTGRES_PASSWORD              # пароль пользователя базы данных
POSTGRES_DB                    # имя базы данных
DB_HOST                        # имя хоста базы данных
DB_PORT                        # порт базы данных
SUPERUSER_USERNAME             # логин администратора
SUPERUSER_EMAIL                # E-mail администратора
SUPERUSER_PASSWORD             # пароль администратора
SUPERUSER_FIRSTNAME            # имя администратора
SUPERUSER_LASTNAME             # фамилия администратора
TELEGRAM_TO                    # id телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN                 # токен бота (получить токен можно у @BotFather, /token, имя бота)
```

При отправке проекта на GitHub в ветку main автоматически отрабатывают сценарии:

* *backend_tests* - проверка кода на соответствие стандарту PEP8 и запуск pytest. Дальнейшие шаги выполняются только если push был в ветку main;
* *build_backend_and_push_to_docker_hub* - сборка и доставка докер-образа backend на DockerHub
* *build_frontend_and_push_to_docker_hub* - сборка и доставка докер-образа frontend на DockerHub
* *deploy* - автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из DockerHub на сервер; Выполняются миграции базы данных; Собирается статика фронтенда и бэкенда; База данных заполняется минимальными необходимыми данными; Создается суперпользователь;
* *send\_message* - отправка уведомления в Telegram.

## Автор
Сергей Иванов.
