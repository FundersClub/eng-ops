from datetime import datetime

from django.db import transaction

from issues.models import Issue

from pipelines.models import (
    Pipeline,
    PipelineState,
)

from api.external_apis import ZenhubApi


def sync_issues():
    minute = datetime.now().minute / 10
    issues = Issue.objects.filter(closed_at__isnull=True)
    for issue in issues:
        #  Hack because Zenhub API
        if issue.id % 6 == minute:
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

    issue.save()
