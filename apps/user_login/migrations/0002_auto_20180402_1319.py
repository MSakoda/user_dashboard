# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-02 20:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_login', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='last',
            new_name='last_name',
        ),
    ]
