"""Dev settings and globals."""

from .base import *


# ######### CELERY CONFIGURATION
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


# ######### CONFIG VARIABLES
ADMIN_URL = 'admin'
SITE_URL = 'site'


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
