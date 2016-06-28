# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 21:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0004_issuecomment'),
        ('repositories', '0002_repository_pipelines'),
        ('api', '0002_githubrequest_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubrequest',
            name='issue_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='issues.IssueComment'),
        ),
        migrations.AddField(
            model_name='githubrequest',
            name='obj_field',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='githubrequest',
            name='repository',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repositories.Repository'),
        ),
    ]