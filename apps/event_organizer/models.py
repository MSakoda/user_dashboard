from __future__ import unicode_literals

import re
import bcrypt

EMAIL_REGEX = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    hashpw = models.CharField(max_length=255)
    user_level = models.IntegerField(default=1)
    friends = models.ManyToManyField('self', related_name = 'friend')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Address(models.Model):
    street = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete = models.SET_NULL, related_name = 'address', null = True, blank = True)

class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

class Event(models.Model):
    created_by_user = models.ForeignKey('User', related_name = 'event', null = True, blank = True)
    indoor = models.BooleanField()
    digital = models.BooleanField()
    number_of_artists = models.SmallIntegerField()
    number_of_guests = models.SmallIntegerField()
    address = models.ForeignKey('Address', related_name = 'event')
    date = models.DateTimeField()
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    contact = models.ForeignKey('Contact', related_name = 'event', null = True, blank = True)
    parking_info = models.TextField()
    border_inquiry = models.TextField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
