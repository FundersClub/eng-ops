from django.db import models


class GithubRequest(models.Model):
    body = models.TextField(null=True, blank=True)
    event = models.CharField(max_length=100)
    handled = models.BooleanField(default=False)
    method = models.CharField(max_length=20)
    time = models.DateTimeField()
