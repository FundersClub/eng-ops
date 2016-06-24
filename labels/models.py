from django.db import models

from repositories.models import Repository


class Label(models.Model):
    name = models.CharField(max_length=50)
    repositories = models.ManyToManyField(Repository, related_name='labels')

    def __unicode__(self):
        return self.name
