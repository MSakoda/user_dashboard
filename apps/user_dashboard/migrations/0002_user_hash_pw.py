# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-06 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hash_pw',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]