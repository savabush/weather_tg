FROM python:3.11

ENV PYTHONUNBUFFERED 1

COPY ./weather_bot /bot

WORKDIR /bot

COPY ./requirements.txt /bot/

RUN pip install --upgrade pip && pip install -r requirements.txt
