# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 22:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pull_requests', '0001_initial'),
        ('api', '0003_auto_20160628_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubrequest',
            name='pull_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pull_requests.PullRequest'),
        ),
    ]
