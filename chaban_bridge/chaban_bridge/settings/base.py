"""
Django settings for chaban_bridge project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
# Built-in
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-bm!!0*x**6p**%&9n(d123t@+uf)-z$th=7!yt(3%8a1s)(crr"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "localhost"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "django_celery_beat",
    "django_celery_results",
    "drf_spectacular",
    "rest_framework",
    # Application
    "core",
    "jobs",
    "user",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "chaban_bridge.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "chaban_bridge.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

POSTGRES_SERVICE_HOST = os.getenv("POSTGRES_SERVICE_HOST", "postgres")
POSTGRES_SERVICE_PORT = os.getenv("POSTGRES_SERVICE_PORT", 5432)
POSTGRES_CHABAN_BRIDGE_USER = os.getenv(
    "POSTGRES_CHABAN_BRIDGE_USER", "chaban_bridge_user"
)
POSTGRES_CHABAN_BRIDGE_PASSWORD = os.getenv(
    "POSTGRES_CHABAN_BRIDGE_PASSWORD", "chaban_bridge_password"
)
POSTGRES_CHABAN_BRIDGE_DB = os.getenv("POSTGRES_CHABAN_BRIDGE_DB", "chaban_bridge")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": POSTGRES_SERVICE_HOST,
        "PORT": POSTGRES_SERVICE_PORT,
        "USER": POSTGRES_CHABAN_BRIDGE_USER,
        "PASSWORD": POSTGRES_CHABAN_BRIDGE_PASSWORD,
        "NAME": POSTGRES_CHABAN_BRIDGE_DB,
    }
}

AUTH_USER_MODEL = "user.User"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Celery

CELERY_CACHE_BACKEND = "default"
CELERY_RESULT_BACKEND = "django-db"

# Channels

ASGI_APPLICATION = "project.asgi.application"
