#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    production = bool(os.getenv('CURRENT_ENVIRONMENT_IS_PRODUCTION', False))
    server_purpose = 'production' if production else 'dev'
    default_settings = "operations.settings.{}".format(server_purpose)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", default_settings)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
