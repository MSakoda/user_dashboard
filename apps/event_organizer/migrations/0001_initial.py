# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-08 21:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('street2', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zipcode', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('hashpw', models.CharField(max_length=255)),
                ('user_level', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='event_organizer.Address')),
                ('friends', models.ManyToManyField(related_name='_user_friends_+', to='event_organizer.User')),
            ],
        ),
    ]
