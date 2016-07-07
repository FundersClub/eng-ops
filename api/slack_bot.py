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
        issue_comments = IssueComment.objects.filter(
            created_at__range=(start_time, end_time),
            user=user,
        ).select_related('issue')
        issue_comment_dict = {}
        for issue_comment in issue_comments:
            issue_comment_dict[issue_comment.issue] = issue_comment_dict.get(issue_comment.issue, 0) + 1

        pr_comments = PullRequestComment.objects.filter(
            created_at__range=(start_time, end_time),
            user=user,
        ).select_related('pull_request')
        pr_comment_dict = {}
        for pr_comment in pr_comments:
            pr_comment_dict[pr_comment.pull_request] = pr_comment_dict.get(pr_comment.pull_request, 0) + 1

        opened_prs = PullRequest.objects.filter(
            closed_at__isnull=True,
            created_at__range=(start_time, end_time),
            user=user,
        )
        closed_prs = PullRequest.objects.filter(
            closed_at__range=(start_time, end_time),
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
        review_prs = PullRequest.objects.filter(
            assignees=user,
            closed_at__isnull=True,
        )
        self_prs = PullRequest.objects.filter(
            closed_at__isnull=True,
            user=user,
        )
        product_backlog_issues = Issue.objects.filter(
            assignee=user,
            closed_at__isnull=True,
            pipeline__name='Product Backlog',
        )
        eng_backlog_issues = Issue.objects.filter(
            assignee=user,
            closed_at__isnull=True,
            pipeline__name='Eng Backlog',
        )

        GITHUB_API_BASE = 'https://github.com/{}/{}/{}/{}/'

        def get_text(objs, copy, obj_type, format_text='%E2%80%A2 {} {}: <{}|{}>'):
            return '\n'.join([format_text.format(
                copy,
                '%23{}'.format(obj.number) if obj_type == 'issues' else 'PR',
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    obj.repository.name,
                    obj_type,
                    obj.number,
                ),
                obj,
            ) for obj in objs])

        recent_issues_text = '\n'.join([
            '*Recent*',
            get_text(opened_issues, 'Opened', 'issues'),
            get_text(closed_issues, 'Closed', 'issues'),
            '\n'.join(['%E2%80%A2 {} comment{} on {} <{}|{}>'.format(
                number,
                's' if number > 1 else '',
                '%23{}'.format(obj.number),
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    obj.repository.name,
                    'issues',
                    obj.number,
                ),
                obj,
            ) for (obj, number) in issue_comment_dict.items()]),
            '',
        ])
        recent_prs_text = '\n'.join([
            get_text(opened_prs, 'Opened', 'pull'),
            get_text(closed_prs, 'Closed', 'pull'),
            '\n'.join(['%E2%80%A2 {} comment{} on <{}|{}>'.format(
                number,
                's' if number > 1 else '',
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    obj.repository.name,
                    'pull',
                    obj.number,
                ),
                obj,
            ) for (obj, number) in pr_comment_dict.items()]),
        ])
        upcoming_text = '\n'.join([
            '*Upcoming*',
            get_text(workon_issues, 'Work on', 'issues'),
            get_text(ready_to_workon_issues, 'Ready to work on', 'issues'),
            get_text(follow_up_issues, 'Follow up on', 'issues'),
            get_text(review_prs, 'Review', 'pull'),
            get_text(self_prs, 'Response to any comments on', 'pull'),
        ])
        backlog_text = '\n'.join([
            '*Backlog*',
            get_text(product_backlog_issues, 'Product backlog', 'issues'),
            get_text(eng_backlog_issues, 'Eng backlog', 'issues'),
        ])

        urls = [SLACK_POST_MESSAGE_BASE_URL.format(
            settings.SLACK_TOKEN,
            '@{}'.format(user.slack_username),
            unicode(text),
            'Standup Bot',
        ) for text in [recent_issues_text, recent_prs_text, upcoming_text, backlog_text]]
        for url in urls:
            requests.get(url)
