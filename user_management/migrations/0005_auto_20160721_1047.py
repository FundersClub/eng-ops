# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 17:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_auto_20160721_1040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='githubuser',
            old_name='login',
            new_name='logins',
        ),
    ]