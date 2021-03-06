# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 21:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_githubuser_slack_username'),
        ('issues', '0005_auto_20160628_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='closed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='closed_issues', to='user_management.GithubUser'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_issues', to='user_management.GithubUser'),
        ),
    ]
