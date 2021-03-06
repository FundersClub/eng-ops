# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 23:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_githubuser_slack_username'),
        ('pull_requests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PullRequestComment',
            fields=[
                ('body', models.TextField(default=b'')),
                ('created_at', models.DateTimeField()),
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('pull_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='pull_requests.PullRequest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.GithubUser')),
            ],
        ),
    ]
