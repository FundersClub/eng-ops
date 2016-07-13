from django.core.management.base import BaseCommand

from api.slack_bot import send_weekly_report


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        send_weekly_report()
