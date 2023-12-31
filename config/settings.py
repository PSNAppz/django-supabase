"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

import environ
import sentry_sdk

from datetime import timedelta

from sentry_sdk.integrations.django import DjangoIntegration


# Django environ

env = environ.Env(
    DEBUG=(bool, True),
    CORS_ORIGIN_ALLOW_ALL=(bool, True),
    CORS_ALLOW_CREDENTIALS=(bool, False),
    CORS_ORIGIN_WHITELIST=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    ACCESS_TOKEN_LIFETIME=(
        dict(cast=dict(minutes=int, hours=int, days=int, weeks=int)),
        {'minutes': 15},
    ),
    REFRESH_TOKEN_LIFETIME=(
        dict(cast=dict(minutes=int, hours=int, days=int, weeks=int,)),
        {'days': 7},
    ),
    PAGE_SIZE=(int, 10),
    CACHE_CONTROL_MAX_AGE=(int, 30 * 1),

    DB_NAME=(str,''),
    DB_HOST=(str,''),
    DB_USER=(str,''),
    DB_PASSWORD=(str,''),
    REDIS_HOST=(str,''),
    SENTRY_DSN=(str, ''),
    CELERY_BROKER_URL=(str, ''),
    CELERY_RESULT_BACKEND=(str, ''),
    FCM_SERVER_KEY=(str, ''),

    SUPABASE_JWT_SECRET=(str, ''),
    SUPABASE_URL=(str, ''),
    SUPABASE_SERVICE_ROLE_KEY=(str, ''),
)

# Read the .env file
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dmi7tj+skkz0r+^n#slnezk46^p92225n2vci94*lfc7oin1vu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*'] #TODO: change this to production domain

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # third party
    'django_extensions',
    'django_summernote',
    'rest_framework',
    'rest_framework.authtoken',
    'adminsortable2',
    'import_export',
    'django_filters',
    'drf_yasg',
    'storages',
    's3direct',
    'corsheaders',
    'fcm_django',
    'imagekit',
    'feincms',
    'djoser',
    'mptt',
    'channels',
    'import_export_celery',
    
    # local
    'users.apps.UsersConfig',
    'supabase_app.apps.SupabaseConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'author.middlewares.AuthorDefaultBackendMiddleware',
    'config.middleware.StatsMiddleware', # Time status middleware
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# Fcm Django
# https://github.com/xtrinch/fcm-django

FCM_DJANGO_SETTINGS = {
    'APP_VERBOSE_NAME': 'Notifications',
    'FCM_SERVER_KEY': env('FCM_SERVER_KEY'),
    'UPDATE_ON_DUPLICATE_REG_ID': True,
    'ONE_DEVICE_PER_USER': True
}


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env('DB_NAME'),
#         'USER': env('DB_USER'),
#         'PASSWORD': env('DB_PASSWORD'),
#         'HOST': env('DB_HOST'),
#         'PORT': '',
#     },
#     #TODO: Update this if required
#     'write': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env('DB_NAME'),
#         'USER': env('DB_USER'),
#         'PASSWORD': env('DB_PASSWORD'),
#         'HOST': env('DB_HOST'),
#         'PORT': '',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.sqlite3',
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3'),
    }
 }

# AWS S3 Storage

# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# # AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=0',
# }
# AWS_LOCATION = 'static'
# AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
# AWS_S3_ENDPOINT_URL = 'https://s3.%s.amazonaws.com' % AWS_S3_REGION_NAME

# S3DIRECT_DESTINATIONS = {
#     'contents': {
        
#         'key': 'contents/',
#         'bucket': env('AWS_STORAGE_BUCKET_NAME'),

#     },
# }

# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_STORAGE = 'config.storage_backends.StaticStorage'
# DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage' 

AUTH_USER_MODEL = 'users.User'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# REST api
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'supabase_app.authentication.SupabaseAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'users.permissions.LimitUserDevices',
        # 'users.permissions.DeactivateUserPermission',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'config.pagination.PageNumberPagination',
    'PAGE_SIZE': env('PAGE_SIZE'),

}

# Djoser Users Auth
# https://djoser.readthedocs.io/en/latest/settings.html

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserMinSerializer',
        'user': 'users.serializers.UserMinSerializer',
        'current_user': 'users.serializers.UserMinSerializer',
    },
    'PERMISSIONS': {
         'user': [
             'djoser.permissions.CurrentUserOrAdminOrReadOnly',
            #  'users.permissions.LimitUserDevices',
         ]
     }
}

# JWT Token Auth
# https://github.com/davesque/django-rest-framework-simplejwt

ACCESS_TOKEN_LIFETIME = env('ACCESS_TOKEN_LIFETIME')
REFRESH_TOKEN_LIFETIME = env('REFRESH_TOKEN_LIFETIME')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(**ACCESS_TOKEN_LIFETIME),
    'REFRESH_TOKEN_LIFETIME': timedelta(**REFRESH_TOKEN_LIFETIME),
    'ROTATE_REFRESH_TOKENS': True,
}

# Djnago Sites
# https://docs.djangoproject.com/en/2.2/ref/contrib/sites/

SITE_ID = 1

# CORS Header
# https://pypi.org/project/django-cors-headers/

CORS_ORIGIN_ALLOW_ALL = env('CORS_ORIGIN_ALLOW_ALL')
CORS_ALLOW_CREDENTIALS = env('CORS_ALLOW_CREDENTIALS')
CORS_ORIGIN_WHITELIST = env('CORS_ORIGIN_WHITELIST')
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS')

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = False

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# User uploaded files (Images, Videos, PDF)
# https://docs.djangoproject.com/en/2.2/topics/files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

IMPORT_EXPORT_CELERY_STORAGE = 'config.storage_backends.ImportExportCeleryStorage'

# django cache page setting user in uitls/cache_page_mixin
# https://www.django-rest-framework.org/api-guide/caching/

CACHE_CONTROL_MAX_AGE = env('CACHE_CONTROL_MAX_AGE')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ASGI_APPLICATION = 'config.asgi.application'
REDIS_HOST = env('REDIS_HOST')
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
                (REDIS_HOST, 6379),
            ],
        },
    },
}
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Celery
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

# Sentry
sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Supabase Credentials
SUPABASE_CONFIG = {
    'SUPABASE_URL':env('SUPABASE_URL'),
    'SUPABASE_SERVICE_ROLE_KEY':env('SUPABASE_SERVICE_ROLE_KEY'),
    'SUPABASE_JWT_SECRET':env('SUPABASE_JWT_SECRET')
}
