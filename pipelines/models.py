from django.db import models


class Pipeline(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
