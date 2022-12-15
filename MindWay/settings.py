"""
Django settings for MindWay project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os, json
from pathlib import Path
import datetime
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# secrets.json get_secrets
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting):
    try :
        return secrets[setting]

    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

# SECRET_KEY
SECRET_KEY = get_secret("SECRET_KEY")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'accounts',
    'applications',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES' : (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}

JWT_AUTH = {
    'JWT_SECRET_KEY' : SECRET_KEY,
    'JWT_ALGORITHM' : 'HS256',
    'JWT_ALLOW_REFRESH' : True,
    'JWT_EXPIRATION_DELTA' : datetime.timedelta(minutes=30),
    'JWT_REFRESH_EXPIRATION_DELTA' : datetime.timedelta(days=28)
}

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MindWay.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR],
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

WSGI_APPLICATION = "MindWay.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'mindway',
        'USER' : get_secret("DATABASE")['USER'],
        'PASSWORD' : get_secret("DATABASE")['PASSWORD'],
        'HOST' : 'localhost',
        'PORT' : '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#logging
DEFAULT_LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : False,
    'loggers' : {
        '' : {
            'level' : 'INFO',
        },
        'another.module' : {
            'level' : 'DEBUG',
        }
    }
}

#SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = '587'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = get_secret("SMTP")['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = get_secret("SMTP")['EMAIL_HOST_PASSWORD']


# Redis Cache
CACHE = {
    'default' : {
        'BACKEND' : 'django_redis.cache.Redis.Cache',
        'LOCATION' : 'redis://127.0.0.1:6379'
    }
}