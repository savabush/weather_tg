FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-traditional

COPY ./weather_app /backend

WORKDIR /backend

COPY ./requirements.txt /backend/
COPY ./weather_app/docker/entrypoint.sh /backend

RUN chmod +x /backend/entrypoint.sh

RUN pip install --upgrade pip && pip install -r requirements.txt
