from django.contrib.postgres.fields import ArrayField
from django.db import models


class GithubUserManager(models.Manager):
    def get_or_create(self, defaults=None, **kwargs):
        if 'login' in defaults:
            defaults['logins'] = [defaults['login']]
            del defaults['login']

        obj, created = super(GithubUserManager, self).get_or_create(defaults, **kwargs)
        if 'logins' in defaults and defaults['logins'][0] not in obj.logins and not created:
            obj.logins.extend(defaults['logins'])
            obj.save()

        return obj, created


class GithubUser(models.Model):

    id = models.PositiveIntegerField(primary_key=True)
    logins = ArrayField(models.CharField(max_length=100, null=True), default=[])
    slack_username = models.CharField(max_length=100, null=True)

    objects = GithubUserManager()

    def __unicode__(self):
        return ', '.join(self.logins)
