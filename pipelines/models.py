from django.db import models


class Pipeline(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class PipelineState(models.Model):
    ended_at = models.DateTimeField(null=True, blank=True)
    issue = models.ForeignKey('issues.Issue', related_name='pipeline_states')
    pipeline = models.ForeignKey(Pipeline)
    started_at = models.DateTimeField()

    def __unicode__(self):
        return '{} {}'.format(
            self.pipeline,
            self.issue,
        )
