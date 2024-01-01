from home_api.settings.base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG')

ALLOWED_HOSTS = [config('ALLOWED_HOSTS'), config('ALLOWED_HOSTS1'), config('SQL_HOST'), config("WWW_HOST"),
                 config('OTHERS_HOSTS')]

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': config('SQL_NAME'),
        'USER': config('SQL_USER'),
        'PASSWORD': config('SQL_PASSWORD'),
        'HOST': config('SQL_HOST'),
        'PORT': config('SQL_PORT'),
    }
}

# settings for product stage

# Connect to Space Digital Ocean
AWS_ACCESS_KEY_ID = config('DO_SPACES_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('DO_SPACES_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'textract-space'
AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": 'max-age=86400',
    'ACL': 'public-read'
}

AWS_LOCATION = 'https://textract-space.fra1.digitaloceanspaces.com'
MEDIA_URL = 'https://textract-space.fra1.digitaloceanspaces.com/media/'
DEFAULT_FILE_STORAGE = "home_api.storages.MediaSpaceStorage"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [config('CSRF_TRUSTED_ORIGINS')]
