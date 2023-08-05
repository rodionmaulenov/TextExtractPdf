FROM python:3.11.4-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    pip install --upgrade pip && \
    apt-get install -y libpq-dev gcc netcat-openbsd

WORKDIR /work_dir

COPY ./requirements.txt /tmx/requirements.txt

RUN pip install -r /tmx/requirements.txt

COPY ./entrypoint.sh /tmx/entrypoint.sh

COPY ./work_dir /work_dir

ENTRYPOINT ["/tmx/entrypoint.sh"]

#FROM python:3.11.4-slim
#
#ENV PYTHONDONTWRITEBYTECODE=1 \
#    PYTHONUNBUFFERED=1
#
#RUN apt-get update && \
#    pip install --upgrade pip && \
#    apt-get install -y libpq-dev gcc netcat-openbsd
#
#WORKDIR /work_dir
#
#COPY --from=builder /tmx/requirements.txt /tmx/requirements.txt
#
#RUN pip install -r /tmx/requirements.txt
#
#COPY ./entrypoint.sh /tmx/entrypoint.sh
#
#COPY ./work_dir /work_dir
#
#ENTRYPOINT ["/tmx/entrypoint.sh"]

