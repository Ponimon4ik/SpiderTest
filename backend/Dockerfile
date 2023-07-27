FROM python:3.10-slim

WORKDIR /app

RUN apt-get update
RUN apt-get -y install libpq-dev gcc

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY city_enterprises/ /app

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
