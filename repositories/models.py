from django.db import models


class Repository(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    private = models.BooleanField()

    class Meta:
        ordering = ('name', )
        verbose_name = 'Repository'
        verbose_name_plural = 'Repositories'

    def __unicode__(self):
        return self.name
