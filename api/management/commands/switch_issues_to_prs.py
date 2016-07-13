import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from issues.models import Issue
from pull_requests.models import PullRequest

from api.models import GithubRequest


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bad_issues = []
        for issue in Issue.objects.all():
            requests = GithubRequest.objects.filter(
                issuecomment__in=issue.comments.all()
            )
            for request in requests:
                content = json.loads(request.body)
                if 'pull_request' in content['issue']:

                    try:
                        pr = PullRequest.objects.get(
                            created_at=issue.created_at,
                            number=issue.number,
                            repository=issue.repository,
                            user=issue.creater,
                        )
                    except ObjectDoesNotExist:
                        pr = PullRequest.objects.create(
                            created_at=issue.created_at,
                            id=issue.id,
                            number=issue.number,
                            repository=issue.repository,
                            user=issue.creater,
                        )
                    finally:
                        pr.body = issue.body
                        pr.closed_at = issue.closed_at
                        pr.title = issue.title
                        if issue.assignee:
                            pr.assignees.add(issue.assignee)
                        pr.save()

                        bad_issues.append(issue.id)
                    break

        Issue.objects.filter(id__in=bad_issues).delete()
