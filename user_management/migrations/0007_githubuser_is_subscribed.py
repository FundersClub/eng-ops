# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-11 23:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0006_auto_20160805_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubuser',
            name='is_subscribed',
            field=models.BooleanField(default=True),
        ),
    ]
