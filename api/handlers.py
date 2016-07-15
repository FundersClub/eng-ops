from datetime import datetime
import unicodedata

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from issues.models import (
    Issue,
    IssueComment,
)
from labels.models import Label
from pipelines.models import (
    Pipeline,
    PipelineState,
)

from pull_requests.models import (
    PullRequest,
    PullRequestComment,
)
from repositories.models import Repository
from user_management.models import GithubUser

from api.external_apis import ZenhubApi


@transaction.atomic
def issue_handler(data):
    issue_data = data['issue']

    assignee = None
    if issue_data['assignee']:
        assignee, _ = GithubUser.objects.get_or_create(
            id=issue_data['assignee']['id'],
            login=issue_data['assignee']['login'],
        )

    creater, _ = GithubUser.objects.get_or_create(
        id=issue_data['user']['id'],
        login=issue_data['user']['login'],
    )

    issue, _ = Issue.objects.update_or_create(
        created_at=issue_data['created_at'],
        creater=creater,
        id=issue_data['id'],
        number=issue_data['number'],
        repository_id=data['repository']['id'],
        defaults={
            'assignee': assignee,
            'body': issue_data['body'],
            'closed_at': issue_data['closed_at'],
            'title': unicodedata.normalize('NFKD', issue_data['title']).encode('ascii', 'ignore'),
        }
    )

    issue.labels.add(
        *Label.objects.filter(
            name__in=[label['name'] for label in issue_data['labels']],
            repositories__id=data['repository']['id'],
        )
    )

    issue.save()
    _sync_issue(issue)

    if issue.closed_at is not None:
        issue.pipeline = Pipeline.objects.get(name='Closed')
        last_pipeline_state = issue.pipeline_states.order_by('started_at').last()
        if last_pipeline_state:
            last_pipeline_state.ended_at = issue.closed_at
            last_pipeline_state.save()
    issue.save()

    return issue


@transaction.atomic
def issue_comment_handler(data):
    if 'pull_request' in data['issue']:
        return pull_request_review_comment_handler(data)

    comment_data = data['comment']
    issue = issue_handler(data)
    user, _ = GithubUser.objects.get_or_create(
        id=comment_data['user']['id'],
        login=comment_data['user']['login'],
    )

    comment, _ = IssueComment.objects.update_or_create(
        created_at=comment_data['created_at'],
        id=comment_data['id'],
        issue=issue,
        user=user,
        defaults={
            'body': comment_data['body'],
        }
    )

    return comment


@transaction.atomic
def pull_request_handler(data):
    pr_data = data['pull_request'] if 'pull_request' in data else data['issue']

    repository = Repository.objects.get(id=data['repository']['id'])
    user, _ = GithubUser.objects.get_or_create(
        id=pr_data['user']['id'],
        login=pr_data['user']['login'],
    )
    assignees = []

    for assignee_data in pr_data['assignees']:
        assignee, _ = GithubUser.objects.get_or_create(
            id=assignee_data['id'],
            login=assignee_data['login'],
        )
        assignees.append(assignee)

    try:
        pull_request = PullRequest.objects.get(
            created_at=pr_data['created_at'],
            number=pr_data['number'],
            repository=repository,
        )
    except ObjectDoesNotExist:
        pull_request = PullRequest.objects.create(
            created_at=pr_data['created_at'],
            id=pr_data['id'],
            number=pr_data['number'],
            repository=repository,

        )
    pull_request.body = pr_data['body']
    pull_request.closed_at = pr_data['closed_at']
    pull_request.merged_at = pr_data.get('merged_at', None)
    pull_request.title = unicodedata.normalize('NFKD', pr_data['title']).encode('ascii', 'ignore'),
    pull_request.user = user
    pull_request.assignees.clear()
    pull_request.assignees.add(*assignees)
    return pull_request


@transaction.atomic
def pull_request_review_comment_handler(data):
    comment_data = data['comment']
    pull_request = pull_request_handler(data)
    user, _ = GithubUser.objects.get_or_create(
        id=comment_data['user']['id'],
        login=comment_data['user']['login'],
    )

    comment, _ = PullRequestComment.objects.update_or_create(
        created_at=comment_data['created_at'],
        id=comment_data['id'],
        pull_request=pull_request,
        user=user,
        defaults={
            'body': comment_data['body'],
        }
    )

    return comment


@transaction.atomic
def repository_handler(data):
    repository_data = data['repository']

    repository, _ = Repository.objects.update_or_create(
        id=repository_data['id'],
        name=repository_data['name'],
        default={
            'private': repository_data['private'],
        }
    )

    return repository


@transaction.atomic
def _sync_issue(issue):
    issue_events = ZenhubApi.get_issue_events(issue.repository_id, issue.number)
    for event in issue_events[::-1]:
        if event['type'] == 'transferIssue':
            if PipelineState.objects.filter(
                    ended_at=event['created_at'],
                    issue=issue,
            ).exists():
                continue

            from_pipeline, _ = Pipeline.objects.get_or_create(name=event['from_pipeline']['name'])
            pipeline_state = PipelineState.objects.filter(
                issue=issue,
                pipeline=from_pipeline,
            ).order_by('started_at').last()
            if not pipeline_state:
                pipeline_state = PipelineState.objects.create(
                    issue=issue,
                    pipeline=from_pipeline,
                    started_at=issue.created_at,
                )
            pipeline_state.ended_at = event['created_at']
            pipeline_state.save()

            to_pipeline, _ = Pipeline.objects.get_or_create(name=event['to_pipeline']['name'])
            pipeline_state = PipelineState.objects.create(
                issue=issue,
                pipeline=to_pipeline,
                started_at=event['created_at'],
            )
            issue.pipeline = to_pipeline
        if event['type'] == 'estimateIssue':
            issue.estimate = event.get('to_estimate', {'value': 0})['value']

    issue_data = ZenhubApi.get_issue(issue.repository_id, issue.number)
    issue.estimate = issue_data.get('estimate', {'value': 0}).get('value')

    if 'pipeline' in issue_data:
        pipeline, _ = Pipeline.objects.get_or_create(name=issue_data['pipeline']['name'])

        if issue.pipeline == pipeline:
            issue.save()
            return

        pipeline_state = PipelineState.objects.filter(
            issue=issue,
            pipeline=pipeline,
        ).order_by('started_at').last()

        event_time = datetime.now() if pipeline_state else issue.created_at
        if pipeline_state:
            pipeline_state.ended_at = event_time
            pipeline_state.save()

        PipelineState.objects.create(
            issue=issue,
            pipeline=pipeline,
            started_at=event_time,
        )

    issue.save()
