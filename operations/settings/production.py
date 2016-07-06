"""Production settings and globals."""

import dj_database_url

from .base import *


# ######### DATABASE CONFIGURATION
DATABASES = {}
DATABASES['default'] = dj_database_url.config()

ALLOWED_HOSTS += [
    host for host in os.getenv('ENG_OPS_ALLOWED_HOSTS').split(',')
]


# ######### DEBUG CONFIGURATION
DEBUG = False


# ######### RAVEN CONFIGURATION
RAVEN_CONFIG = {
    'auto_log_stacks': True,
    'dsn': os.getenv('RAVEN_DSN'),
    'processors': (
        'raven.processors.SanitizePasswordsProcessor',
    ),
    'release': raven.VERSION,
    'string_max_length': 5000,
    'timeout': 5,
}
