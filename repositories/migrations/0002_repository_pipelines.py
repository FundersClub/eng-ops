# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-27 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipelines', '0001_initial'),
        ('repositories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='pipelines',
            field=models.ManyToManyField(related_name='repositories', to='pipelines.Pipeline'),
        ),
    ]