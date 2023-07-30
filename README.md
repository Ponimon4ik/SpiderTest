# SpiderTest
Тестовое задание для Spider


### Используемые технологии:

+ Django,
+ Django rest framework
+ Python
+ Docker

### Установка Docker:

Установите Docker
```
sudo apt install docker
```

Установите docker-compose, с этим вам поможет [официальная документация](https://docs.docker.com/compose/install/)

### Как запустить проект:

Клонировать репозиторий и перейти в директорию infra:
```
git clone https://github.com/Ponimon4ik/SpiderTest
```
```
cd infra/
```

Cоздать env-файл и прописать переменные окружения в нём:
```
touch .env
```
```
SECRET_KEY='django-insecure-x)b42fn*!l$w&#4v7@5a-58hp75yk95&$=zf-3@$$%b34kz22q'
DEBUG_STATUS=0
ALLOWED_HOSTS=*

DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=city_enterprises
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Запустить docker-compose
```
docker-compose up -d
```

Создать супер юзера:
```
docker-compose exec web python3 manage.py createsuperuser
```


### Как загрузить тестовые данные:

Выполнить команду:
```
docker-compose exec web python3 manage.py loaddata fixtures.json
```

### Документация к API:

Документация к API доступна по адресу http://localhost/api/v1/swagger/

### Как запустить тесты к API:

Перейти в корень проекта SpiderTest и выполнить команду.
Выполнять только после сборки docker-compose
```
pytest
```


### Автор:

+ Стефанюк Богдан