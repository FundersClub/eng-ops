from django.db import models

from labels.models import Label
from pipelines.models import Pipeline
from repositories.models import Repository
from user_management.models import GithubUser


class Issue(models.Model):

    assignee = models.ForeignKey(GithubUser, null=True, blank=True, related_name='assigned_issues')
    body = models.TextField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    closed_by = models.ForeignKey(GithubUser, null=True, blank=True, related_name='closed_issues')
    created_at = models.DateTimeField()
    creater = models.ForeignKey(GithubUser, related_name='created_issues')
    estimate = models.PositiveSmallIntegerField(default=0)
    id = models.PositiveIntegerField(primary_key=True)
    labels = models.ManyToManyField(Label, related_name='issues')
    number = models.PositiveSmallIntegerField()
    pipeline = models.ForeignKey(Pipeline, null=True, related_name='issues')
    repository = models.ForeignKey(Repository, related_name='issues')
    title = models.CharField(max_length=256)

    class Meta:
        ordering = (
            'repository',
            '-number',
        )

    def __unicode__(self):
        return ('{}: {}'.format(
            self.repository,
            self.title,
        ).replace('#', '')
            .replace('<', '')
            .replace('>', '')
            .replace('\r', '')
            .replace('\n', '')
            .replace('&', '')
        )


class IssueComment(models.Model):
    body = models.TextField(default='')
    created_at = models.DateTimeField()
    id = models.PositiveIntegerField(primary_key=True)
    issue = models.ForeignKey(Issue, related_name='comments')
    user = models.ForeignKey(GithubUser)

    def __unicode__(self):
        return '{} - {}'.format(
            self.user,
            self.issue,
        )
