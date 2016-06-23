"""Production settings and globals."""

import dj_database_url

from .base import *


# ######### DATABASE CONFIGURATION
DATABASES = {}
DATABASES['default'] = dj_database_url.config()


# ######### DEBUG CONFIGURATION
DEBUG = False
