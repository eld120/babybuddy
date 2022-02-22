import os 
from distutils.util import strtobool

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

import environ
import logging, sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
env.read_env(BASE_DIR / ".env")
# Environment variables
# Check for and load environment variables from a .env file.
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))


load_dotenv(find_dotenv())

# Required settings

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or None
DEBUG = bool(strtobool(os.environ.get('DEBUG') or 'False'))


# Applications
# https://docs.djangoproject.com/en/3.0/ref/applications/

INSTALLED_APPS = [
    'api',
    'babybuddy',
    'core',
    'dashboard',
    'reports',

    "anymail",
    'axes',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',
    'easy_thumbnails',
    'storages',
    'import_export',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

# Middleware
# https://docs.djangoproject.com/en/3.0/ref/middleware/

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'babybuddy.middleware.RollingSessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'babybuddy.middleware.UserTimezoneMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'babybuddy.middleware.UserLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]


# URL dispatcher
# https://docs.djangoproject.com/en/3.0/topics/http/urls/

ROOT_URLCONF = 'babybuddy.urls'


# Templates
# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-TEMPLATES

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        
        'OPTIONS': {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# # Database
# # https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# config = {
#     'ENGINE': os.getenv('DB_ENGINE') or 'django.db.backends.sqlite3',
#     'NAME': os.getenv('DB_NAME') or os.path.join(BASE_DIR, 'data/db.sqlite3')
# }
# if os.getenv('DB_USER'):
#     config['USER'] = os.getenv('DB_USER')
# if os.environ.get('DB_PASSWORD') or os.environ.get('POSTGRES_PASSWORD'):
#     config['PASSWORD'] = os.environ.get('DB_PASSWORD') or os.environ.get('POSTGRES_PASSWORD')
# if os.getenv('DB_HOST'):
#     config['HOST'] = os.getenv('DB_HOST')
# if os.getenv('DB_PORT'):
#     config['PORT'] = os.getenv('DB_PORT')

# DATABASES = {'default': config}

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Cache
# https://docs.djangoproject.com/en/3.0/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_default',
    }
}


# WGSI
# https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/

WSGI_APPLICATION = 'babybuddy.wsgi.application'


# Authentication
# https://docs.djangoproject.com/en/3.0/topics/auth/default/

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = 'babybuddy:root-router'

LOGIN_URL = 'babybuddy:login'

LOGOUT_REDIRECT_URL = 'babybuddy:login'


# Timezone
# https://docs.djangoproject.com/en/3.0/topics/i18n/timezones/

USE_TZ = True

TIME_ZONE = os.environ.get('TIME_ZONE') or 'UTC'


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

USE_I18N = True

LANGUAGE_CODE = 'en-US'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

LANGUAGES = [
    ('en-US', _('English (US)')),
    ('en-GB', _('English (UK)')),
    ('nl', _('Dutch')),
    ('fr', _('French')),
    ('fi', _('Finnish')),
    ('de', _('German')),
    ('it', _('Italian')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('es', _('Spanish')),
    ('sv', _('Swedish')),
    ('tr', _('Turkish'))
]


# Format localization
# https://docs.djangoproject.com/en/3.0/topics/i18n/formatting/

USE_L10N = True

# Custom setting that can be used to override the locale-based time set by
# USE_L10N _for specific locales_ to use 24-hour format. In order for this to
# work with a given locale it must be set at the FORMAT_MODULE_PATH with
# conditionals on this setting. See babybuddy/forms/en/formats.py for an example
# implementation for the English locale.

USE_24_HOUR_TIME_FORMAT = bool(strtobool(os.environ.get('USE_24_HOUR_TIME_FORMAT') or 'False'))


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# http://whitenoise.evans.io/en/stable/django.html

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WHITENOISE_ROOT = os.path.join(BASE_DIR, 'static', 'babybuddy', 'root')

WHITENOISE_MANIFEST_STRICT = False

# Media files (User uploaded content)
# https://docs.djangoproject.com/en/3.0/topics/files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'

# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME') or None

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') or None

# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') or None

# if AWS_STORAGE_BUCKET_NAME:
#     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#     THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# Security

# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-proxy-ssl-header
if os.environ.get('SECURE_PROXY_SSL_HEADER'):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# https://docs.djangoproject.com/en/3.2/topics/http/sessions/#settings
SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/3.2/ref/csrf/#settings
CSRF_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/3.2/topics/auth/passwords/
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Django Rest Framework
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_METADATA_CLASS': 'api.metadata.APIMetadata',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': [
        'api.permissions.BabyBuddyDjangoModelPermissions'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'PAGE_SIZE': 100
}

# Import/Export configuration
# See https://django-import-export.readthedocs.io/

IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'add'

IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'change'

IMPORT_EXPORT_USE_TRANSACTIONS = True

# Axes configuration
# See https://django-axes.readthedocs.io/en/latest/4_configuration.html

AXES_COOLOFF_TIME = 1

AXES_FAILURE_LIMIT = 5

# Session configuration
# Used by RollingSessionMiddleware to determine how often to reset the session.
# See https://docs.djangoproject.com/en/3.0/topics/http/sessions/

ROLLING_SESSION_REFRESH = 86400

# Set default auto field for models.
# See https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Baby Buddy configuration
# See README.md#configuration for details about these settings.

BABY_BUDDY = {
    'NAP_START_MIN': os.environ.get('NAP_START_MIN') or '06:00',
    'NAP_START_MAX': os.environ.get('NAP_START_MAX') or '18:00',
    'ALLOW_UPLOADS': bool(strtobool(os.environ.get('ALLOW_UPLOADS') or 'True'))
}


# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

ANYMAIL = {
    "SENDGRID_API_KEY": env("SENDGRID_API_KEY"),
}

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
integrations = [
    sentry_logging,
    DjangoIntegration(),
    
]
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=integrations,
    environment=env("SENTRY_ENVIRONMENT", default="production"),
    #traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
    traces_sample_rate=1.0
)

ADMIN_URL = env("DJANGO_ADMIN_URL")

if DEBUG == True:
    from .base import *
    from .base import env

    ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"] + ALLOWED_HOSTS

    INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405

    # django-debug-toolbar
    # ------------------------------------------------------------------------------
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
    INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
    if env("USE_DOCKER") == "yes":
        import socket

        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

    # django-extensions
    # ------------------------------------------------------------------------------
    # https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
    INSTALLED_APPS += ["django_extensions"]  # noqa F405