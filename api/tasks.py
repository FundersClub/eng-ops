from django.db import transaction

from issues.models import Issue

from pipelines.models import (
    Pipeline,
    PipelineState,
)

from api.external_apis import ZenhubApi


def sync_issues():
    # issues = Issue.objects.filter(closed_at__isnull=True)
    issues = Issue.objects.filter(
        repository__name='eng-ops',
        number='22',
    )

    for issue in issues:
        sync_issue(issue)


@transaction.atomic
def sync_issue(issue):
    issue_events = ZenhubApi.get_issue_events(issue.repository_id, issue.number)
    for event in issue_events[::-1]:
        if event['type'] == 'transferIssue':
            if PipelineState.objects.filter(ended_at=event['created_at']).exists():
                continue

            from_pipeline, _ = Pipeline.objects.get_or_create(name=event['from_pipeline']['name'])
            pipeline_state = PipelineState.objects.filter(
                issue=issue,
                pipeline=from_pipeline,
            ).order_by('started_at').last()
            pipeline_state.ended_at = event['created_at']
            pipeline_state.save()

            to_pipeline, _ = Pipeline.objects.get_or_create(name=event['to_pipeline']['name'])
            pipeline_state, _ = PipelineState.objects.create(
                issue=issue,
                pipeline=to_pipeline,
                started_at=event['created_at'],
            )
            issue.pipeline = to_pipeline
        if event['type'] == 'estimateIssue':
            issue.estimate = event['to_estimate']['value']

    issue.save()
