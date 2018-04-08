from __future__ import unicode_literals

import re
import bcrypt

EMAIL_REGEX = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'


from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        print "postData:"
        print postData
        errors = {}
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Email is invalid"
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name must be at least 3 characters"
        if len(postData['first_name']) < 3:
            errors['last_name'] = "Last name must be at least 3 characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 3 characters"
        if postData['password'] != postData['pw_conf']:
            errors['pw_conf'] = "Passwords don't match!"
        return errors

    def user_exist_check(self, postData):
        errors = {}
        user = User.objects.filter(email__iexact = postData['email'])
        if len(user):
            errors['email'] = "That email has already been taken"
        print "Email is not taken"
        return errors

    def user_add(self, postData):
        users = User.objects.all()
        if len(users) < 1:
            print "no users yet, make this user an admin"
            user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], hash_pw = bcrypt.hashpw( postData['password'].encode(), bcrypt.gensalt()), user_level = 9)
            return
        else:
            user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], hash_pw = bcrypt.hashpw( postData['password'].encode(), bcrypt.gensalt()), user_level = 0)
            return user

    def get_user_by_email(self, email):
        user = User.objects.filter(email__iexact=email)
        if len(user) < 1:
            return "User not in database"
        else:
            return user

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    hash_pw = models.CharField(max_length = 255)
    user_level = models.IntegerField()
    desc = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class MessageManager(models.Manager):
    def validate_message(self, postData):
        print "validating message"
        return


class Message(models.Model):
    message = models.TextField(default='')
    message_by = models.ForeignKey(User, related_name = 'message_by')
    message_to = models.ForeignKey(User, related_name = 'message_to')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()

class CommentManager(models.Manager):
    def validate_comment(self, postData):
        print "validating comment"
        return

class Comment(models.Model):
    comment = models.TextField(default='')
    comment_by = models.ForeignKey(User, related_name = 'comment_by')
    message = models.ForeignKey(Message, related_name = 'comment')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CommentManager()
