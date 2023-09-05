FROM python:3.11.4-slim-buster

WORKDIR /home/app/web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE home_api.settings.docker_stage_settings

RUN apt-get update && apt-get install -y netcat default-jre

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
