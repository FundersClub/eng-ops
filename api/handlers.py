from django.db import transaction

from issues.models import (
    Issue,
    IssueComment,
)
from labels.models import Label
from pipelines.models import Pipeline
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

    issue, _ = Issue.objects.get_or_create(
        created_at=issue_data['created_at'],
        creater=creater,
        id=issue_data['id'],
        number=issue_data['number'],
        repository_id=data['repository']['id'],
    )

    issue.assignee = assignee
    issue.body = issue_data['body']
    issue.title = issue_data['title']
    issue.closed_at = issue_data['closed_at']
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


def issue_comment_handler(data):
    comment_data = data['comment']
    issue = Issue.objects.get(id=data['issue']['id'])
    user, _ = GithubUser.objects.get_or_create(
        id=comment_data['user']['id'],
        login=comment_data['user']['login'],
    )

    comment, _ = IssueComment.objects.get_or_create(
        created_at=comment_data['created_at'],
        issue=issue,
        user=user,
    )
    comment.body = comment_data['body']
    comment.save()

    return comment


@transaction.atomic
def repository_handler(data):
    repository_data = data['repository']

    repository, _ = Repository.objects.get_or_create(
        id=repository_data['id'],
        name=repository_data['name'],
    )

    repository.private = repository_data['private']
    repository.save()

    return repository
