from home_api.cdn.conf import *
from home_api.settings.base import *


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS'), os.environ.get('SQL_HOST'), os.environ.get("WWW_HOST"),
                 os.environ.get('OTHERS_HOSTS')]


DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': os.environ.get('SQL_NAME'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [os.environ.get('CSRF_TRUSTED_ORIGINS')]


STORAGES = {
    "default": {
        "BACKEND": "home_api.cdn.backends.MediaRootS3BotoStorage",
        "OPTIONS": {
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
            "AWS_STORAGE_BUCKET_NAME": AWS_STORAGE_BUCKET_NAME,
            "AWS_S3_ENDPOINT_URL": AWS_S3_ENDPOINT_URL,
            "AWS_S3_OBJECT_PARAMETERS": AWS_S3_OBJECT_PARAMETERS,
            "AWS_LOCATION": AWS_LOCATION,
        },
    },
}

STATICFILES_STORAGE = 'home_api.cdn.backends.StaticRootS3BotoStorage'


