from datetime import (
    datetime,
    timedelta,
)

from django.conf import settings
from django.db.models import Q

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

SLACK_POST_MESSAGE_BASE_URL = 'https://slack.com/api/chat.postMessage?token={}&channel={}&text={}&as_user=True&username={}'


def send_standup_messages():
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1, hours=1)

    for user in GithubUser.objects.filter(slack_username__isnull=False):
        opened_issues = Issue.objects.filter(
            assignee=user,
            closed_at__isnull=True,
            created_at__range=(start_time, end_time),
        )
        closed_issues = Issue.objects.filter(
            Q(closed_at__range=(start_time, end_time)) &
            (
                Q(assignee=user) |
                Q(closed_by=user)
            )
        )
        opened_prs = PullRequest.objects.filter(
            closed_at__isnull=True,
            created_at__range=(start_time, end_time),
            user=user,
        )
        workon_issues = Issue.objects.filter(
            assignee=user,
            closed_at__isnull=True,
            pipeline__in=Pipeline.objects.filter(name__in=['In Progress', 'In Review']),
        )
        ready_to_workon_issues = Issue.objects.filter(
            assignee=user,
            closed_at__isnull=True,
            pipeline__name='Ready to do',
        )
        follow_up_issues = Issue.objects.filter(
            assignee=user,
            closed_at__isnull=True,
            pipeline__in=Pipeline.objects.filter(name__in=['Requires Followup', 'New Issues']),
        )
        product_backlog_issues = Issue.objects.filter(
            assignee=user,
            closed_at__isnull=True,
            pipeline__name='Product backlog',
        )
        eng_backlog_issues = Issue.objects.filter(
            assignee=user,
            closed_at__isnull=True,
            pipeline__name='Eng backlog',
        )

        GITHUB_API_BASE = 'https://github.com/{}/{}/{}/{}'

        text = '\n'.join([
            '',
            '*Recent*',
            '\n'.join(['%E2%80%A2 Opened %23{}: <{}|{}>'.format(
                issue.number,
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    issue.repository.name,
                    'issues',
                    issue.number,
                ),
                issue.short_name,
            ) for issue in opened_issues]),
            '\n'.join(['%E2%80%A2 Closed %23{}: <{}|{}>'.format(
                issue.number,
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    issue.repository.name,
                    'issues',
                    issue.number,
                ),
                issue.short_name,
            ) for issue in closed_issues]),
            '\n'.join(['%E2%80%A2 Opened PR: <{}|{}>'.format(
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    pr.repository.name,
                    'pull',
                    pr.number,
                ),
                pr.short_name,
            ) for pr in opened_prs]),
            '',
            '*Upcoming*',
            '\n'.join(['%E2%80%A2 Work on %23{}: <{}|{}>'.format(
                issue.number,
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    issue.repository.name,
                    'issues',
                    issue.number,
                ),
                issue.short_name,
            ) for issue in workon_issues]),
            '\n'.join(['%E2%80%A2 Ready to work on %23{}: <{}|{}>'.format(
                issue.number,
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    issue.repository.name,
                    'issues',
                    issue.number,
                ),
                issue.short_name,
            ) for issue in ready_to_workon_issues]),
            '\n'.join(['%E2%80%A2 Follow up on %23{}: <{}|{}>'.format(
                issue.number,
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    issue.repository.name,
                    'issues',
                    issue.number,
                ),
                issue.short_name,
            ) for issue in follow_up_issues]),
            '',
            '*Backlog*',
            '\n'.join(['%E2%80%A2 Product backlog %23{}: <{}|{}>'.format(
                issue.number,
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    issue.repository.name,
                    'issues',
                    issue.number,
                ),
                issue.short_name,
            ) for issue in product_backlog_issues]),
            '\n'.join(['%E2%80%A2 Eng backlog %23{}: <{}|{}>'.format(
                issue.number,
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    issue.repository.name,
                    'issues',
                    issue.number,
                ),
                issue.short_name,
            ) for issue in eng_backlog_issues]),
        ])
        url = SLACK_POST_MESSAGE_BASE_URL.format(
            settings.SLACK_TOKEN,
            '@{}'.format(user.slack_username),
            unicode(text),
            'Standup Bot',
        )
        requests.get(url)
