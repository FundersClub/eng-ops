"""
WSGI config for fcopps project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

production = bool(os.getenv('CURRENT_ENVIRONMENT_IS_PRODUCTION', False))
server_purpose = 'production' if production else 'dev'
default_settings = "operations.settings.{}".format(server_purpose)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", default_settings)


from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())
