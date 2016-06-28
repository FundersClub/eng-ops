from django.db import transaction

from issues.models import Issue
from labels.models import Label
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
    issue.save()

    return issue


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
