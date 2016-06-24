from django.db import models


class GithubUser(models.Model):

    id = models.PositiveIntegerField(primary_key=True)
    login = models.CharField(max_length=100)

    def __unicode__(self):
        return self.login
