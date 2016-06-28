from django.db import models


class GithubUser(models.Model):

    id = models.PositiveIntegerField(primary_key=True)
    login = models.CharField(max_length=100)
    slack_username = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.login
