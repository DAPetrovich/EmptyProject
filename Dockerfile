FROM python:3.8

RUN pip install fastapi uvicorn
COPY ./app /app

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
