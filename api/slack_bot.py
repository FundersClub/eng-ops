#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import (
    datetime,
    timedelta,
)
import json
import logging

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

logger = logging.getLogger(__name__)
SLACK_POST_MESSAGE_BASE_URL = 'https://slack.com/api/chat.postMessage'
SLACK_POST_DATA = {
    'as_user': 'True',
    'token': settings.SLACK_TOKEN,
    'username': 'Standup%20Bot',
}


def send_standup_messages():
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)

    for user in GithubUser.objects.filter(slack_username__isnull=False):
        opened_issues = Issue.objects.filter(
            creater=user,
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
            pipeline__name='Ready To Do',
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

        GITHUB_API_BASE = 'https://github.com/{}/{}/{}/{}'

        def get_text(objs, copy, obj_type, format_text='• {} {}: <{}|{}>'):
            return '\n'.join([format_text.format(
                copy,
                '#{}'.format(obj.number) if obj_type == 'issues' else 'PR',
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    obj.repository.name,
                    obj_type,
                    obj.number,
                ),
                obj,
            ) for obj in objs])

        recent_text = [
            '*Recent*',
            get_text(opened_issues, 'Opened', 'issues'),
            get_text(closed_issues, 'Closed', 'issues'),
            '\n'.join(['• {} comment{} on {} <{}|{}>'.format(
                number,
                's' if number > 1 else '',
                '#{}'.format(obj.number),
                GITHUB_API_BASE.format(
                    settings.GITHUB_ORGANIZATION,
                    obj.repository.name,
                    'issues',
                    obj.number,
                ),
                obj,
            ) for (obj, number) in issue_comment_dict.items()]),
            get_text(opened_prs, 'Opened', 'pull'),
            get_text(closed_prs, 'Closed', 'pull'),
            '\n'.join(['• {} comment{} on <{}|{}>'.format(
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
        ]
        upcoming_text = [
            '*Upcoming*',
            get_text(workon_issues, 'Work on', 'issues'),
            get_text(ready_to_workon_issues, 'Ready to work on', 'issues'),
            get_text(follow_up_issues, 'Follow up on', 'issues'),
            get_text(review_prs, 'Review', 'pull'),
            get_text(self_prs, 'Respond to any comments on', 'pull'),
        ]
        backlog_text = [
            '*Backlog*',
            get_text(product_backlog_issues, 'Product backlog', 'issues'),
            get_text(eng_backlog_issues, 'Eng backlog', 'issues'),
        ]

        text = '\n'.join([line for text_set in [recent_text, upcoming_text, backlog_text] for line in text_set if line != ''])
        post_data = SLACK_POST_DATA.copy()
        post_data['channel'] = '@{}'.format(user.slack_username)
        post_data['text'] = text

        response = requests.post(SLACK_POST_MESSAGE_BASE_URL, data=post_data)
        if not json.loads(response.content)['ok']:
            logger.error('Could not send standup message to {}'.format(user.slack_username))
