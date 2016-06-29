from datetime import (
    datetime,
    timedelta,
)

from django.conf import settings

import requests

from issues.models import (
    Issue,
    IssueComment,
)
from pipelines.models import Pipeline
from pull_requests.models import (
    PullRequest,
    PullRequestComment,
)
from user_management.models import GithubUser

SLACK_POST_MESSAGE_BASE_URL = 'https://slack.com/api/chat.postMessage?token={}&channel={}&text={}&username={}'


def send_standup_messages():
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1, hours=1)

    for user in GithubUser.objects.filter(slack_username__isnull=False):
        open_issues = Issue.objects.filter(
            closed_at__isnull=True,
            assignee=user,
        )
        closed_issues = Issue.objects.filter(
            closed_at__range=(start_time, end_time),
            assignee=user,
        )
        closed_pull_requests = PullRequest.objects.filter(
            closed_at__range=(start_time, end_time),
            user=user,
        )
        opened_pull_requests = PullRequest.objects.filter(
            created_at__range=(start_time, end_time),
            user=user,
        )
        issue_comments = IssueComment.objects.filter(
            created_at__range=(start_time, end_time),
            user=user,
        ).count()
        pull_request_comments = PullRequestComment.objects.filter(
            created_at__range=(start_time, end_time),
            user=user,
        ).count()

        text = '\n'.join([
            '*Closed issues:* \n>{}'.format(
                '\n>'.join([str(issue) for issue in closed_issues])
            ),
            '*Opened pull requests:* \n>{}'.format(
                '\n>'.join([str(pull_request) for pull_request in opened_pull_requests])
            ),
            '*Closed pull requests:* \n>{}'.format(
                '\n>'.join([str(pull_request) for pull_request in closed_pull_requests])
            ),
            '*Pipeline Issues*:\n',
            '\n'.join([
                '>*{}*: {} issues'.format(pipeline, open_issues.filter(pipeline=pipeline).count()) for pipeline in Pipeline.objects.all() if open_issues.filter(pipeline=pipeline).exists()]),
            '*{} issue comments*'.format(issue_comments),
            '*{} pull request comments*'.format(pull_request_comments),
        ])
        requests.get(SLACK_POST_MESSAGE_BASE_URL.format(
            settings.SLACK_TOKEN,
            '@{}'.format(user.slack_username),
            text,
            'Standup Bot',
        ))
