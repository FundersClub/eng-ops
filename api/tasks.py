from issues.models import Issue
from labels.models import Label
from repositories.models import Repository
from user_management.models import GithubUser

from api.external_apis import GithubApi


def sync_all():
    sync_repos()
    sync_all_labels()
    sync_all_issues()


def sync_repos():
    repos_data = GithubApi.get_all_repos()
    for repo_data in repos_data:
        Repository.objects.get_or_create(
            id=repo_data['id'],
            name=repo_data['name'],
            private=repo_data['private'],
        )


def sync_all_labels():
    for repo in Repository.objects.all():
        labels_data = GithubApi.get_repo_labels(repo.name)
        for label_data in labels_data:
            label, _ = Label.objects.get_or_create(
                name=label_data['name'],
            )
            label.repositories.add(repo)
            label.save()


def sync_all_issues():
    for repo in Repository.objects.all():
        sync_issues(repo)


def sync_issues(repo):
    issues_data = GithubApi.get_repo_issues(repo)
    for issue_data in issues_data:
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
            assignee=assignee,
            body=issue_data['body'],
            closed_at=issue_data.get('closed_at', None),
            created_at=issue_data['created_at'],
            creater=creater,
            id=issue_data['id'],
            number=issue_data['number'],
            repository=repo,
            title=issue_data['title'],
        )
        issue.labels.clear()
        issue.labels.add(
            *Label.objects.filter(
                name__in=[label['name'] for label in issue_data['labels']],
                repositories__in=[repo],
            )
        )
        issue.save()
