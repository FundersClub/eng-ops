"""Dev settings and globals."""

from .base import *


# ######### CELERY CONFIGURATION
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


# ######### DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eng-ops',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS += [
    'localhost',
]


# ######### URL CONFIGURATION
BASE_URL = 'http://localhost:4000'
