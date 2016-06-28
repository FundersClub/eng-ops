from django.db import models

from repositories.models import Repository
from user_management.models import GithubUser


class PullRequest(models.Model):
    assignees = models.ManyToManyField(GithubUser, related_name='assigned_pull_requests')
    body = models.TextField(default='')
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField()
    id = models.PositiveIntegerField(primary_key=True)
    merged_at = models.DateTimeField(null=True, blank=True)
    number = models.PositiveIntegerField()
    repository = models.ForeignKey(Repository)
    title = models.CharField(max_length=256)
    user = models.ForeignKey(GithubUser, related_name='pull_requests')

    def __unicode__(self):
        return '{}: {}'.format(
            self.repository,
            self.title,
        )

