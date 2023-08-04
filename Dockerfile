FROM python:3.11.4-slim

RUN mkdir /work_dir
WORKDIR /work_dir

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN apt-get update && \
    pip install --upgrade pip && \
    apt-get install -y libpq-dev gcc netcat-openbsd

COPY ./requirements.txt /tmx/requirements.txt
COPY ./entrypoint.sh /tmx/entrypoint.sh

RUN pip install -r /tmx/requirements.txt

COPY ./work_dir /work_dir

ENTRYPOINT ["/tmx/entrypoint.sh"]

