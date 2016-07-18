#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import (
    datetime,
    timedelta,
)
import json
import logging
import operator

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
GITHUB_API_BASE = 'https://github.com/{}/{}/{}/{}'
SLACK_POST_MESSAGE_BASE_URL = 'https://slack.com/api/chat.postMessage'
SLACK_POST_DATA = {
    'as_user': 'True',
    'token': settings.SLACK_TOKEN,
    'username': 'Standup%20Bot',
}


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


def send_message(text, user):
    post_data = SLACK_POST_DATA.copy()
    post_data['channel'] = '@{}'.format(user.slack_username)
    post_data['text'] = text

    response = requests.post(SLACK_POST_MESSAGE_BASE_URL, data=post_data)
    if not json.loads(response.content)['ok']:
        logger.error('Could not send standup message to {}'.format(user.slack_username))
        return False
    return True


def send_standup_messages():
    end_time = datetime.now()

    if end_time.weekday() > 4:  # weekend
        return
    if end_time.weekday() == 0:  # Monday
        start_time = end_time - timedelta(days=3)
    else:
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
        send_message(text, user)


def _create_label_dict(issues):
    issue_breakdown_dict = {}
    for issue in issues:
        for label in issue.labels.all():
            issue_breakdown_dict[label.name] = issue_breakdown_dict.get(label.name, 0) + 1.0
        if issue.labels.all().count() == 0:
            issue_breakdown_dict['None'] = issue_breakdown_dict.get('None', 0) + 1.0
    return issue_breakdown_dict


def send_weekly_report():
    end_time = datetime.now()
    if end_time.weekday() != 0:
        return

    start_date = end_time - timedelta(days=28)
    weeks = (end_time - start_date).days / 7.0

    start_time = end_time - timedelta(days=7)
    last_week = end_time - timedelta(days=14)

    closed_issues = Issue.objects.filter(
        closed_at__range=(start_time, end_time),
    ).prefetch_related('labels')
    closed_issues_count = closed_issues.count()
    issue_breakdown_dict = _create_label_dict(closed_issues)

    team_accomplishments = [
        '*Team Accomplishments*',
        'Opened {} issues (Avg: {}, Last week: {})'.format(
            Issue.objects.filter(
                created_at__range=(start_time, end_time),
            ).count(),
            Issue.objects.filter(
                created_at__range=(start_date, end_time),
            ).count() / weeks,
            Issue.objects.filter(
                created_at__range=(last_week, start_time),
            ).count(),
        ),
        'Closed {} issues (Avg: {}, Last week: {})'.format(
            closed_issues_count,
            Issue.objects.filter(
                closed_at__range=(start_date, end_time),
            ).count() / weeks,
            Issue.objects.filter(
                closed_at__range=(last_week, start_time),
            ).count(),
        ),
        'Completed {} points (Avg: {}, Last week: {})'.format(
            sum([issue.estimate for issue in closed_issues]),
            sum([issue.estimate for issue in Issue.objects.filter(
                closed_at__range=(start_date, end_time),
            )]) / weeks,
            sum([issue.estimate for issue in Issue.objects.filter(
                closed_at__range=(last_week, start_time),
            )]),
        ),
        '',
        '\n'.join(['• {} {}, {}%'.format(
            label_name,
            int(number),
            round(100 * number / closed_issues_count, 2),
        ) for (label_name, number) in sorted(
            issue_breakdown_dict.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )]),
        '',
    ]

    for user in GithubUser.objects.filter(slack_username__isnull=False):
        user_closed_issues = Issue.objects.filter(
            Q(closed_at__range=(start_time, end_time)) &
            (
                Q(assignee=user) |
                Q(closed_by=user)
            )
        ).prefetch_related('labels')
        user_issue_breakdown_dict = _create_label_dict(user_closed_issues)

        user_closed_issues_count = user_closed_issues.count()
        personal_accomplishments = [
            '*Personal Report*',
            'Opened {} issues (Avg: {}, Last week: {})'.format(
                Issue.objects.filter(
                    created_at__range=(start_time, end_time),
                    creater=user,
                ).count(),
                Issue.objects.filter(
                    created_at__range=(start_date, end_time),
                    creater=user,
                ).count() / weeks,
                Issue.objects.filter(
                    created_at__range=(last_week, start_time),
                    creater=user,
                ).count(),
            ),
            'Closed {} issues (Avg: {}, Last week: {})'.format(
                user_closed_issues_count,
                Issue.objects.filter(
                    Q(closed_at__range=(start_date, end_time)) &
                    (
                        Q(assignee=user) |
                        Q(closed_by=user)
                    )
                ).count() / weeks,
                Issue.objects.filter(
                    Q(closed_at__range=(last_week, start_time)) &
                    (
                        Q(assignee=user) |
                        Q(closed_by=user)
                    )
                ).count(),
            ),
            'Completed {} points (Avg: {}, Last week: {})'.format(
                sum([issue.estimate for issue in user_closed_issues]),
                sum([issue.estimate for issue in Issue.objects.filter(
                    Q(closed_at__range=(start_date, end_time)) &
                    (
                        Q(assignee=user) |
                        Q(closed_by=user)
                    )
                )]) / weeks,
                sum([issue.estimate for issue in Issue.objects.filter(
                    Q(closed_at__range=(last_week, start_time)) &
                    (
                        Q(assignee=user) |
                        Q(closed_by=user)
                    )
                )]),
            ),
            '',
            '\n'.join(['• {} {}, {}%'.format(
                label_name,
                int(number),
                round(100 * number / user_closed_issues_count, 2),
            ) for (label_name, number) in sorted(
                user_issue_breakdown_dict.items(),
                key=operator.itemgetter(1),
                reverse=True,
            )]),
        ]

        text = '\n'.join(team_accomplishments + personal_accomplishments)
        send_message(text, user)
