from django.core.exceptions import ObjectDoesNotExist

from pull_requests.models import PullRequest


def transfer_as_pr(modeladmin, request, queryset):
    for issue in queryset:
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

    queryset.delete()
