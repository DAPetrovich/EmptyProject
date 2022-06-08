
Запускаем Docker
```shell script
docker-compose up --build
```

Запускаем сервер Uvicorn
```shell script
uvicorn src.main:app --reload
```

Создание миграций
```shell script
alembic revision --autogenerate
```

Применение миграций
```shell script
alembic upgrade head