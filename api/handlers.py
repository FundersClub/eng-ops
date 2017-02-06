import unicodedata

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from issues.models import (
    Issue,
    IssueComment,
)
from labels.models import Label

from pull_requests.models import (
    PullRequest,
    PullRequestComment,
)
from repositories.models import Repository
from user_management.models import GithubUser


def no_action_handler(data):
    return None


@transaction.atomic
def issue_handler(data):
    issue_data = data['issue']

    assignee = None
    if issue_data['assignee']:
        assignee, _ = GithubUser.objects.get_or_create(
            id=issue_data['assignee']['id'],
            defaults={
                'login': issue_data['assignee']['login'],
            },
        )

    creater, _ = GithubUser.objects.get_or_create(
        id=issue_data['user']['id'],
        defaults={
            'login': issue_data['user']['login'],
        },
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

    for label in issue_data['labels']:
        label_obj, created = Label.objects.get_or_create(
            name=label['name'],
        )
        if created:
            label_obj.repositories.add(data['repository']['id'])
        issue.labels.add(label_obj)

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
        defaults={
            'login': comment_data['user']['login'],
        },
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
        defaults={
            'login': pr_data['user']['login'],
        },
    )
    assignees = []

    for assignee_data in pr_data['assignees']:
        assignee, _ = GithubUser.objects.get_or_create(
            id=assignee_data['id'],
            defaults={
                'login': assignee_data['login'],
            },
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
            user=user,
        )
    pull_request.body = pr_data['body']
    pull_request.closed_at = pr_data['closed_at']
    pull_request.merged_at = pr_data.get('merged_at', None)
    pull_request.title = unicodedata.normalize('NFKD', pr_data['title']).encode('ascii', 'ignore')
    pull_request.user = user
    pull_request.assignees.clear()
    pull_request.assignees.add(*assignees)
    pull_request.save()
    return pull_request


@transaction.atomic
def pull_request_review_comment_handler(data):
    comment_data = data['comment']
    pull_request = pull_request_handler(data)
    user, _ = GithubUser.objects.get_or_create(
        id=comment_data['user']['id'],
        defaults={
            'login': comment_data['user']['login'],
        },
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
        defaults={
            'private': repository_data['private'],
        }
    )

    return repository
