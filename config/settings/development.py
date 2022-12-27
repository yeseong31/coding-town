from dj_database_url import config

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv('LOCAL_DB_ENGINE'),
        'NAME': os.getenv('LOCAL_DB_NAME'),
        'USER': os.getenv('LOCAL_DB_USER'),
        'PASSWORD': os.getenv('LOCAL_DB_PASSWORD'),
        'HOST': os.getenv('LOCAL_DB_HOST'),
        'PORT': int(os.getenv('LOCAL_DB_PORT')),
    }
}

db_from_env = config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
