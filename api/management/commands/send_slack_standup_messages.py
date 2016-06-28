from django.core.management.base import BaseCommand

from api.slack_bot import send_standup_messages


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        send_standup_messages()
