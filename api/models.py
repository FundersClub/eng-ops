from django.db import models

from issues.models import (
    Issue,
    IssueComment,
)
from pull_requests.models import (
    PullRequest,
    PullRequestComment,
)
from repositories.models import Repository


class GithubRequest(models.Model):
    action = models.CharField(max_length=50, default='')
    body = models.TextField(null=True, blank=True)
    event = models.CharField(max_length=100)
    handled = models.BooleanField(default=False)
    issue = models.ForeignKey(Issue, null=True, blank=True, related_name='requests')
    issuecomment = models.ForeignKey(IssueComment, null=True, blank=True, related_name='requests')
    method = models.CharField(max_length=20)
    obj_field = models.CharField(max_length=50, null=True, blank=True)
    pullrequest = models.ForeignKey(PullRequest, null=True, blank=True, related_name='requests')
    pullrequestcomment = models.ForeignKey(PullRequestComment, null=True, blank=True, related_name='requests')
    repository = models.ForeignKey(Repository, null=True, blank=True)
    time = models.DateTimeField()

    class Meta:
        ordering = ('time', )

    def save(self, *args, **kwargs):
        for attr in [
                'issue',
                'issuecomment',
                'pullrequest',
                'pullrequestcomment',
                'repository',
        ]:
            if getattr(self, attr, None) is not None:
                self.obj_field = attr
                break
        super(GithubRequest, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} - {}:{}'.format(
            self.time, self.repository, self.action
        )
