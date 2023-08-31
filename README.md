# SkyEng test task

![workflow](https://github.com/ThatCoderMan/skyeng_test_task/actions/workflows/flake8.yml/badge.svg)
![workflow](https://github.com/ThatCoderMan/skyeng_test_task/actions/workflows/deploy.yml/badge.svg)

<details>
<summary>Project stack</summary>

- Python 3.9
- Django 4.2
- Celery 5.3
- Celery Beat 2.5
- Flake8
- Reportlab 4.0
- Docker Compose
- Gunicorn
- Nginx
- PostgresQL
- GitHub Actions

</details>


## Описание
Сервис проверки соответствия python кода общепринятым правилам (PEP8).
Пользователь может зарегистрироваться в сервисе, загрузить .py файл и 
получить на почту результат проверки кода с замечаниями.

### Инструкция по запуску:
Клонируйте репозиторий:
```commandline
git clone git@github.com:ThatCoderMan/skyeng_test_task.git
```

Перейти в папку *infra/*:
```commandline
cd infra/
```
Разверните контейнеры при помощи docker-compose:
```commandline
docker-compose up -d --build
```
Выполните миграции, соберите файлы статики:
```commandline
docker-compose exec django python manage.py migrate
docker compose exec -T web python manage.py collectstatic --no-input
```

### Остановка контейнеров:
```commandline
sudo docker-compose stop
```

### резервная копия базы данных
```commandline
docker-compose exec django python manage.py dumpdata > fixtures.json 
```

### Заполнение .env файла
В корневой папке необходимо создать `.env` файл и заполнить его данными как в примере `.env.example`:
```dotenv
SECRET_KEY="SECRET_KEY"
CSRF_TRUSTED="127.0.0.1"
DEBUG="True"
DB_ENGINE="django.db.backends.postgresql"
DB_NAME="postgres"
DB_USER="postgres"
POSTGRES_PASSWORD="postgres"
DB_HOST="postgresql"
DB_PORT="5432"
CELERY_BROKER_URL="redis://redis:6379/0"
CELERY_RESULT_BACKEND="redis://redis:6379/0"
```

#### Авторы проекта:

- [Артемий Березин](https://github.com/ThatCoderMan)