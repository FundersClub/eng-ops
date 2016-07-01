from django.core.management.base import BaseCommand

from api.tasks import retry_failed_requests


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        retry_failed_requests()
