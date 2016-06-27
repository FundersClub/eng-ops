from django.core.management.base import BaseCommand

from api.tasks import sync_all


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sync_all()
