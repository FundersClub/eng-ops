# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 23:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='title',
            field=models.CharField(max_length=256),
        ),
    ]
