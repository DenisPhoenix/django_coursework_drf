import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# путь корневой директории
BASE_DIR = Path(__file__).resolve().parent.parent

# секретные настройки проекта
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", default="False") == "True"

# разрешенные хоста
ALLOWED_HOSTS = []

# встроенные приложения Django
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# сторонние библиотеки
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_celery_beat",
]
# приложения проекта
LOCAL_APPS = [
    "users.apps.UsersConfig",
]

# Все установленные приложения
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# настройки запросов
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# главный urls.py
ROOT_URLCONF = "config.urls"

# настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# настройки БД
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("NAME"),
        "USER": os.getenv("USER"),
        "PASSWORD": os.getenv("PASSWORD"),
        "HOST": os.getenv("HOST"),
        "PORT": os.getenv("PORT"),
    }
}

# валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# настройки интернациональности
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# статика
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

# медиа
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# модель пользователя
AUTH_USER_MODEL = "users.User"

# настройки DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# JWT-токен
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# настройка документации API
SPECTACULAR_SETTINGS = {
    "TITLE": "API трекер полезных привычек",
    "DESCRIPTION": "API в котором пользователи приобретают новые полезные привычки и "
    "искорененные старые плохие привычки",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# настройки Redis
CACHE_ENABLED = os.getenv("CACHE_ENABLED", default="False") == "True"
if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": os.getenv("CACHE_BACKEND"),
            "LOCATION": os.getenv("CACHE_LOCATION"),
        }
    }

# настройки для Celery worker
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = os.getenv("CELERY_TASK_TRACK_STARTED", default="False") == "True"
CELERY_TASK_TIME_LIMIT = int(os.getenv("CELERY_TASK_TIME_LIMIT_MINUTES", default=5)) * 60

# настройки для Celery beat
CELERY_BEAT_SCHEDULE = {
    "user-block": {
        "task": "my_app.tasks.my_func",
        "schedule": timedelta(days=1),
    },
}

# настройки отправки сообщений на Gmail
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", default="False") == "True"
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", default="False") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
