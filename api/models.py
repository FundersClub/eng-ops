from django.db import models

from issues.models import (
    Issue,
    IssueComment,
)
from pull_requests.models import PullRequest
from repositories.models import Repository


class GithubRequest(models.Model):
    body = models.TextField(null=True, blank=True)
    event = models.CharField(max_length=100)
    handled = models.BooleanField(default=False)
    issue = models.ForeignKey(Issue, null=True, blank=True)
    issue_comment = models.ForeignKey(IssueComment, null=True, blank=True)
    method = models.CharField(max_length=20)
    obj_field = models.CharField(max_length=50, null=True, blank=True)
    pullrequest = models.ForeignKey(PullRequest, null=True, blank=True)
    repository = models.ForeignKey(Repository, null=True, blank=True)
    time = models.DateTimeField()

    def save(self, *args, **kwargs):
        for attr in [
                'issue',
                'issue_comment',
                'pullrequest',
                'repository',
        ]:
            if getattr(self, attr, None) is not None:
                self.obj_field = attr
                break
        super(GithubRequest, self).save(*args, **kwargs)
