FROM alpine:latest

RUN mkdir /code
WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE home_api.settings.test

COPY . .

RUN apk add --update-cache \
    python3 \
    python3-dev \
    py-pip \
    build-base \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*




#FROM python:3.9.18-alpine
#ENV PYTHONUNBUFFERED 1
#ENV DJANGO_SETTINGS_MODULE home_api.settings.test
#RUN mkdir /code
#WORKDIR /code
#COPY . .
#
#RUN apk --no-cache add --virtual .build-deps \
#    ca-certificates \
#    gcc \
#    g++ \
#    postgresql-dev \
#    linux-headers \
#    musl-dev \
#    libffi-dev \
#    jpeg-dev \
#    zlib-dev \
#    make \
#    && pip install -r requirements.txt \
#    && find /usr/local \
#        \( -type d -a -name test -o -name tests \) \
#        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
#        -exec rm -rf '{}' + \
#    && runDeps="$( \
#        scanelf --needed --nobanner --recursive /usr/local \
#                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
#                | sort -u \
#                | xargs -r apk info --installed \
#                | sort -u \
#    )" \
#    && apk add --virtual .rundeps $runDeps \
#    && apk del .build-deps




