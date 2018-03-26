"""
Django settings for jeffchenseo project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
ROOT_DIR = environ.Path(__file__) - 2
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Setting up environment variables
env = environ.Env()
environ.Env.read_env(env_file=ROOT_DIR('.env'))

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['jeffchenseo-dev.us-west-2.elasticbeanstalk.com',
                 '127.0.0.1',
                 'localhost',
                 '.jeffchenseo.com']

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',  # Add in ability to add sitemaps
    'django.contrib.sites'  # Sites framework for django
]
THIRD_PARTY_APPS = [
    'storages',  # App for S3
    'bootstrap4',  # Bootstrap plugin
    'debug_toolbar',  # Debugging tool
    'django_elasticsearch_dsl',  # Elasticsearch plugin
    'crispy_forms',  # Makes forms look cool
    'send_email',  # Sends emails
    'raven.contrib.django.raven_compat',  # Error reporting
    'export_action'  # Export data to CSVs
]
LOCAL_APPS = [
    'jeffchenseo',
    'votes'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = 'jeffchenseo.urls'

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

WSGI_APPLICATION = 'jeffchenseo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'jeffchenseo',
            'USER': 'jeffchen',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Pacific'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images) All Custom Below
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "..", "www", "media")

# AWS Connections
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'elasticbeanstalk-us-west-2-928248191884'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'jeffchenseo.storage_backends.StaticStorage'
STATIC_URL = '/static/'

DEFAULT_FILE_STORAGE = 'jeffchenseo.storage_backends.MediaStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = '/media/'

AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

SITE_ID = 1

# Debug Toolbar Settings
INTERNAL_IPS = [
    '127.0.0.1',
]

# Elasticsearch
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'https://search-jeffchenseo-fsfpr6cxqth4fcp3ujkxk3ljyq.us-west-2.es.amazonaws.com'
    },
}

# Send Email
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = env('MAILGUN_ACCESS_KEY')
MAILGUN_SERVER_NAME = 'email.jeffchenseo.com'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Sentry
RAVEN_CONFIG = {
    'dsn': 'https://9f31b4c4a93c41adbe1f600eae839740:b618b88188884213af7fd57706c37e8b@sentry.io/238311',
}

# This is your actual Project ID and Write Key
import keen

keen.project_id = env('KEEN_PROJECT_ID')
keen.write_key = env('KEEN_WRITE_KEY')

# AWS Signing
import sys, hashlib, hmac

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

# Import Local Development Settings
try:
    from jeffchenseo.local_settings import *
except ImportError:
    pass
