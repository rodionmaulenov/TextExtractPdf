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


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'text-extract-pdf-spaces'
AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read"
}
AWS_LOCATION = "https://text-extract-pdf-spaces.fra1.digitaloceanspaces.com"
DEFAULT_FILE_STORAGE = "home_api.storages.MediaRootS3BotoStorage"
STATICFILES_STORAGE = 'home_api.storages.StaticRootS3BotoStorage'
