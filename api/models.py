from django.db import models

from issues.models import Issue


class GithubRequest(models.Model):
    body = models.TextField(null=True, blank=True)
    event = models.CharField(max_length=100)
    handled = models.BooleanField(default=False)
    issue = models.ForeignKey(Issue, null=True, blank=True)
    method = models.CharField(max_length=20)
    time = models.DateTimeField()
