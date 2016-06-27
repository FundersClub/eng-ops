from django.db import models

from pipelines.models import Pipeline


class Repository(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    pipelines = models.ManyToManyField(Pipeline, related_name='repositories')
    private = models.BooleanField()

    class Meta:
        ordering = ('name', )
        verbose_name = 'Repository'
        verbose_name_plural = 'Repositories'

    def __unicode__(self):
        return self.name
