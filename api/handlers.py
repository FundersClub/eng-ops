from django.db import transaction

from issues.models import (
    Issue,
    IssueComment,
)
from labels.models import Label
from pipelines.models import Pipeline
from pull_requests.models import PullRequest
from repositories.models import Repository
from user_management.models import GithubUser


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
            'title': issue_data['title'],
        }
    )

    issue.labels.add(
        *Label.objects.filter(
            name__in=[label['name'] for label in issue_data['labels']],
            repositories__id=data['repository']['id'],
        )
    )

    if issue.closed_at is not None:
        issue.pipeline = Pipeline.objects.get(name='Closed')
    issue.save()

    return issue


@transaction.atomic
def issue_comment_handler(data):
    comment_data = data['comment']
    issue = Issue.objects.get(id=data['issue']['id'])
    user, _ = GithubUser.objects.get_or_create(
        id=comment_data['user']['id'],
        login=comment_data['user']['login'],
    )

    comment, _ = IssueComment.objects.update_or_create(
        created_at=comment_data['created_at'],
        issue=issue,
        user=user,
        default={
            'body': comment_data['body'],
        }
    )

    return comment


@transaction.atomic
def pull_request_handler(data):
    pr_data = data['pull_request']

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

    pull_request, _ = PullRequest.objects.update_or_create(
        created_at=pr_data['created_at'],
        id=pr_data['id'],
        number=pr_data['number'],
        repository=repository,
        defaults={
            'body': pr_data['body'],
            'closed_at': pr_data['closed_at'],
            'merged_at': pr_data['merged_at'],
            'title': pr_data['title'],
            'user': user,
        }
    )

    pull_request.assignees.clear()
    pull_request.assignees.add(*assignees)
    return pull_request


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
