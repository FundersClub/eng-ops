from django.db import models

from labels.models import Label
from repositories.models import Repository
from user_management.models import GithubUser


class Issue(models.Model):

    assignee = models.ForeignKey(GithubUser, null=True, blank=True, related_name='issues')
    body = models.TextField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField()
    creater = models.ForeignKey(GithubUser, related_name='created_issues')
    id = models.PositiveIntegerField(primary_key=True)
    labels = models.ManyToManyField(Label, related_name='issues')
    number = models.PositiveSmallIntegerField()
    repository = models.ForeignKey(Repository, related_name='issues')
    title = models.CharField(max_length=256)

    class Meta:
        ordering = (
            'repository',
            '-number',
        )
