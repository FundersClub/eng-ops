from issues.models import Issue
from labels.models import Label
from pipelines.models import Pipeline
from repositories.models import Repository
from user_management.models import GithubUser

from api.external_apis import (
    GithubApi,
    ZenhubApi,
)


def sync_all():
    #sync_repos()
    #sync_all_labels()
    #sync_all_issues()
    #sync_all_boards()


def sync_all_issues():
    for repo in Repository.objects.all():
        sync_issues(repo)


def sync_all_labels():
    for repo in Repository.objects.all():
        labels_data = GithubApi.get_repo_labels(repo.name)
        for label_data in labels_data:
            label, _ = Label.objects.get_or_create(
                name=label_data['name'],
            )
            label.repositories.add(repo)
            label.save()


def sync_all_boards():
    for repo in Repository.objects.all():
        sync_boards(repo)


def sync_boards(repo):
    pipelines_data = ZenhubApi.get_boards(repo.id)['pipelines']
    for pipeline_data in pipelines_data:
        pipeline, _ = Pipeline.objects.get_or_create(
            name=pipeline_data['name'],
        )
        repo.pipelines.add(pipeline)

        issue_estimate_dict = {
            issue['issue_number']: issue.get('estimate', {'value': 0}).get('value') for issue in pipeline_data['issues']
        }

        issues = Issue.objects.filter(
            number__in=[issue['issue_number'] for issue in pipeline_data['issues']],
            repository_id=repo.id,
        )
        pipeline.issues.add(*issues)
        for issue in issues:
            issue.estimate = issue_estimate_dict[issue.number]
            issue.save()


def sync_issues(repo):
    issues_page = 1
    issues_data = GithubApi.get_repo_issues(repo, issues_page)
    while len(issues_data) > 0:
        for issue_data in issues_data:
            if issue_data.get('pull_request', None) is not None:
                continue
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
                repository=repo,
            )
            Issue.objects.filter(id=issue.id).update(
                assignee=assignee,
                body=issue_data['body'],
                closed_at=issue_data.get('closed_at', None),
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
        issues_page += 1
        issues_data = GithubApi.get_repo_issues(repo, issues_page)


def sync_repos():
    repos_data = GithubApi.get_all_repos()
    for repo_data in repos_data:
        Repository.objects.get_or_create(
            id=repo_data['id'],
            name=repo_data['name'],
            private=repo_data['private'],
        )
