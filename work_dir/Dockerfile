FROM python:3.9.18-alpine as builder
WORKDIR /code
COPY . .

RUN apk --no-cache add --virtual .build-deps \
    make \
    ca-certificates \
    gcc \
    g++ \
    postgresql-dev \
    linux-headers \
    mupdf-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -v -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps



FROM python:3.9.18-alpine
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=home_api.settings.test

WORKDIR /code
COPY --from=builder /usr/local /usr/local
COPY . .

# Install runtime dependencies
RUN apk add --no-cache \
    postgresql-libs \
    mupdf \
    libstdc++




