from issues.models import Issue

from api.external_apis import ZenhubApi


def sync_issues():
    issues = Issue.objects.filter(closed_at__isnull=True)

    for issue in issues:
        issue_events = ZenhubApi.get_issue_events(issue.repository_id, issue.number)
        for event in issue_events:
            if event['type'] == 'transferIssue':
                continue
            if event['type'] == 'estimateIssue':
                continue
