# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GithubUser',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=100)),
            ],
        ),
    ]