
docker-compose up --build

uvicorn src.main:app --reload

Создание миграций
```shell script
alembic revision --autogenerate
```

Применение миграций
```shell script
alembic upgrade head