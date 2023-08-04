FROM python:3.11.4-alpine

WORKDIR /work_dir

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apk add postgresql-dev build-base postgresql-client

COPY ./requirements.txt /tmx/requirements.txt

RUN pip install -r /tmx/requirements.txt

COPY ./work_dir /work_dir



