"""
Django settings for kimei project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-74x&l$-3%y^n^e#!ux^w_mnwb#3t4=07ed8x6i(-z-d4hj9*ti'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local app
    'gmao.apps.GmaoConfig',
    "accounts.apps.AccountsConfig",
    "gmao_teams.apps.GmaoTeamsConfig",
    "api.apps.ApiConfig",
    "gmao.templatetags",

    # third party 
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_crontab',
    'channels',
    # external

    'django_flatpickr',
    'bootstrap5',
    'fontawesome_5',
    'fontawesomefree',
    'crispy_forms',
    'crispy_bootstrap5',
    'cryptography',
    'django_browser_reload',
]
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
# }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'gmao.middleware.SessionExpirationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'accounts.middleware.SessionValidationMiddleware'
]

ROOT_URLCONF = 'kimei.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'kimei.wsgi.application'
# ASGI_APPLICATION = 'kimei.asgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',

    },
    'auth_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auth_db_name',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
    },
    'kimei_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kimei',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',

        #        'HOST': 'localhostt',
    },
    'teams_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'teams',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        # 'HOST': 'kimei.softether.net',
    },
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.dummy',
#
#     },
#     'auth_db': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'auth_db_name',
#         'USER': 'Daniel',
#         'PASSWORD': 'Mei*2030',
#         'HOST': 'kimei.softether.net',
#     },
#     'kimei_db': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'mei',
#         'USER': 'root',
#         # 'PASSWORD': 'Mei*2030',
#         'HOST': '192.168.30.41',
#
#         #        'HOST': 'localhostt',
#     },
#     'teams_db': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'teams',
#         'USER': 'Daniel',
#         'PASSWORD': 'Mei*2030',
#         'HOST': 'kimei.softether.net',
#         # 'HOST': 'kimei.softether.net',
#     },
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.dummy',
#
#     },
#     'auth_db': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'auth_db_name',
#         'USER': 'root',
#         'PASSWORD': 'Mei*2080',
#         'HOST': 'localhost',
#     },
#     'kimei_db': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'kimei',
#         'USER': 'root',
#         'PASSWORD': 'Mei*2080',
#         'HOST': 'localhost',
#
#         #        'HOST': 'localhostt',
#     },
#     'teams_db': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'teams',
#         'USER': 'root',
#         'PASSWORD': 'Mei*2080',
#         'HOST': 'localhost',
#     },
# }
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Etc/GMT-3'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'gmao' / 'static',
    BASE_DIR / 'accounts' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_REDIRECT_URL = 'gmao:home'
LOGOUT_REDIRECT_URL = 'accounts:index'
# Paramètres de session
SESSION_COOKIE_AGE = 86400  # Durée de vie du cookie de session en secondes (1 jour)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # La session expire à la fermeture du navigateur
SESSION_SAVE_EVERY_REQUEST = True  # Sauvegarde la session à chaque requête
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "accounts.Employee"
DATABASE_ROUTERS = ['routers.db_routers.AuthRouter',
                    'routers.db_routers.KimeiRouter',
                    'routers.db_routers.TeamsRouter',
                    ]
AUTHENTICATION_BACKENDS = [
    'accounts.auth.PersonnelAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://kimei.softether.net:8000", ]
CORS_ALLOW_ALL_ORIGINS = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
