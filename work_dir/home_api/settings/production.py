from .base import *

# SECRET_KEY = os.environ.get('SECRET_KEY')
# DEBUG = os.environ.get('DEBUG')
# ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]
#
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
#
# CSRF_TRUSTED_ORIGINS = [os.environ.get('CSRF_TRUSTED_ORIGINS')]
#
#
# DATABASES = {
#     'default': {
#         'ENGINE': "django.db.backends.postgresql_psycopg2",
#         'NAME': os.environ.get('SQL_NAME'),
#         'USER': os.environ.get('SQL_USER'),
#         'PASSWORD': os.environ.get('SQL_PASSWORD'),
#         'HOST': os.environ.get('SQL_HOST'),
#         'PORT': os.environ.get('SQL_PORT'),
#     }
# }


SECRET_KEY = 'django-insecure-fy!otfu*^lbwn_%vav4rw+d$8%4afj4j5rme&$(&eh$8jh4nea'
DEBUG = False
ALLOWED_HOSTS = ["myproject.kyiv.ua"]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = ["myproject.kyiv.ua"]

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': 'defaultdb',
        'USER': 'doadmin',
        'PASSWORD': 'AVNS_d1gf5rnE8h6ri163FhA',
        'HOST': 'db-postgresql-text-extract-pdf-do-user-14589010-0.b.db.ondigitalocean.com',
        'PORT': '25060',
    }
}
