from django.utils import timezone

from issues.models import Issue

from api.handlers import _sync_issue
from api.models import GithubRequest
from api.views import handle_request


def sync_issues():
    minute = timezone.now().minute / 10
    issues = Issue.objects.filter(closed_at__isnull=True)
    for issue in issues:
        #  Hack because Zenhub API
        if issue.id % 6 == minute:
            _sync_issue(issue)


def retry_failed_requests():
    failed_requests = GithubRequest.objects.filter(handled=False)
    for failed_request in failed_requests:
        try:
            handle_request(failed_request)
        except AttributeError as e:
            continue
