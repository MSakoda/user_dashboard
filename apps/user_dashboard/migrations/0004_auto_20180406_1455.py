# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-06 21:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0003_auto_20180406_0925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='user',
            new_name='message_by',
        ),
        migrations.AddField(
            model_name='message',
            name='message_to',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='message_to', to='user_dashboard.User'),
            preserve_default=False,
        ),
    ]
