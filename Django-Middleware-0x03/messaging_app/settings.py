# messaging_app/settings.py

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# QUICK-START DEVELOPMENT SETTINGS
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# A new key is generated here. If you have your old one, you can use it.
SECRET_KEY = 'django-insecure-p!$7-@n6f@t+s(5*o5w1v*+d&r)i%5x$j#w@y@h5z_q)x^o'

# SECURITY WARNING: don't run with debug turned on in production!
# Setting DEBUG to True fixes the "ALLOWED_HOSTS" error for local development.
DEBUG = True

ALLOWED_HOSTS = []


# APPLICATION DEFINITION

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps you installed
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',

    # Your local apps
    'chats',
]

# === YOUR MIDDLEWARE CONFIGURATION IS HERE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Your middleware is correctly placed here
    'chats.middleware.RequestLoggingMiddleware', 
]

ROOT_URLCONF = 'messaging_app.urls'

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

WSGI_APPLICATION = 'messaging_app.wsgi.application'


# === DATABASE CONFIGURATION FIX ===
# This adds the default SQLite database, fixing the "DATABASES is improperly configured" error.
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# === REST FRAMEWORK CONFIGURATION (For JWT Authentication) ===
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


# === YOUR LOGGING CONFIGURATION IS HERE ===
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'requests.log', # Creates the log file in your project root
            'formatter': 'simple',
        },
    },
    'formatters': {
        'simple': {
            'format': '{message}',
            'style': '{',
        },
    },
    'loggers': {
        'chats.middleware': {  # This matches the logger name from `getLogger(__name__)`
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}