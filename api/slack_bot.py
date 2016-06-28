from datetime import (
    datetime,
    timedelta,
)

from django.conf import settings

import requests

from issues.models import Issue
from user_management.models import GithubUser

SLACK_POST_MESSAGE_BASE_URL = 'https://slack.com/api/chat.postMessage?token={}&channel={}&text={}&username={}'


def send_standup_messages():
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1, hours=1)

    for user in GithubUser.objects.all():
        if not user.slack_username:
            continue

        issues = Issue.objects.filter(
            closed_at__range=(start_time, end_time),
            assignee=user,
        )
        requests.get(SLACK_POST_MESSAGE_BASE_URL.format(
            settings.SLACK_TOKEN,
            '@{}'.format(user.slack_username),
            'You have closed the following issues: \n{}'.format(
                '\n'.join([str(issue) for issue in issues])
            ),
            'Standup Bot',
        ))
