import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', False) == 'True'

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django_apscheduler',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mailing',
    'users',
    'blog'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('NAME_DB'),  # Название БД
        'USER': os.getenv('USER_DB'),  # Пользователь для подключения
        'PASSWORD': os.getenv('PASSWORD_DB'),  # Пароль для этого пользователя
        'HOST': os.getenv('HOST'),  # Адрес, на котором развернут сервер БД
        'PORT': os.getenv('PORT'),  # Порт, на котором работает сервер БД
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = os.getenv('TIME_ZONE')

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = "/"  # Переадресация на главную страницу при авторизации
LOGOUT_REDIRECT_URL = "/"  # Переадресация на главную страницу при выходе из системы
LOGIN_URL = "/users/login"  # Переадресация на страницу авторизации

EMAIL_HOST = os.getenv("EMAIL_HOST")  # Адрес сервера
EMAIL_PORT = os.getenv("EMAIL_PORT")  # Порт сервера
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # Пользователь сервера
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # Пароль сервера для отправки писем
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False) == "True"  # Включить TLS
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", False) == "True"  # Включить SSL

SERVER_EMAIL = EMAIL_HOST_USER  # Наименование сервера
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Адрес отправителя

CACHE_ENABLED = True  # Включить кэш

if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.getenv("LOCATION"),
        }
    }
