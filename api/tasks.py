from issues.models import Issue
from pipelines.models import Pipeline
from repositories.models import Repository

from api.external_apis import ZenhubApi


def sync_all():
    sync_all_boards()


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
