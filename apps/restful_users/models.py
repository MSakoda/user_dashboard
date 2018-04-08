from __future__ import unicode_literals
import re

EMAIL_REGEX = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

from django.db import models

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        print "postData:"
        print postData
        errors = {}
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name must be at least 3 characters"
        if len(postData['first_name']) < 3:
            errors['last_name'] = "Last name must be at least 3 characters"
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Email is invalid"
        return errors

    def user_exist_check(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if len(user):
            errors['email'] = "That email has already been taken"
        return errors

    def user_add(self, postData):
        user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'])
        return

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
