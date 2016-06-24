"""Common settings and globals."""

import os
import socket


# ######### SETTINGS
ALLOWED_HOSTS = []
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True
ROOT_DIR = os.path.dirname(BASE_DIR)
ROOT_URLCONF = 'operations.urls'
SITE_ID = 1
WSGI_APPLICATION = 'operations.wsgi.application'


# ######### AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


# ######### CONFIG VARIABLES
CURRENT_ENVIRONMENT_IS_PRODUCTION = os.getenv('CURRENT_ENVIRONMENT_IS_PRODUCTION')
ENG_OPS_GITHUB_KEY = os.getenv('ENG_OPS_GITHUB_KEY')
ENG_OPS_ZENHUB_KEY = os.getenv('ENG_OPS_ZENHUB_KEY')
GITHUB_ORGANIZATION = os.getenv('GITHUB_ORGANIZATION')
SECRET_KEY = os.getenv('ENG_OPS_DJANGO_SECRET_KEY')


# ######### HOST VARIABLES
hostname = socket.gethostname()
hostname = hostname.split('.')[0] if '.' in hostname else hostname


# ######### INSTALLED APPS CONFIGURATION
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
]

LOCAL_APPS = [
    'operations',
    'issues',
    'labels',
    'repositories',
    'user_management',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ######### CELERY CONFIGURATION
CELERY_HIJACK_ROOT_LOGGER = False


# ######### INTERNATIONALIZATION CONFIGURATION
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ######### LOGGING CONFIGURATION
LOGGING = {
    'disable_existing_logging': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(filename)s \t %(funcName)s:%(lineno)d \t %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': False,
    },
    'version': 1,
}


# ######### MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

# ######### REST CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}


# ######### STATIC CONFIGURATION
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'static-root')


# ######### TEMPLATE CONFIGURATION
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
