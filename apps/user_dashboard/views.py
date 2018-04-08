from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime
import bcrypt

import re

EMAIL_REGEX = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

from models import *
# Create your views here.
def index(request):
    return render(request, 'user_dashboard/index.html')

def signin(request):
    if request.method == 'GET':
        context = {
            'messages' : messages.get_messages(request)
        }
        return render(request, 'user_dashboard/signin.html', context)
    else:
        print "attempting to sign in"
        print request.POST['email']
        print request.POST['password']
        user = User.objects.get_user_by_email(request.POST['email'])
        print "user after get:"
        print user
        if user == False:
            messages.error(request, "User is not in database")
            return redirect(reverse('user_dashboard:sign_in'))
        else:
            hash_pw = user[0].hash_pw
            password = request.POST['password']
            if bcrypt.checkpw(password.encode(), hash_pw.encode()):
                messages.success(request, "Successfully logged in")
                request.session['logged_in'] = True
                request.session['user_id'] = user[0].id
                request.session['user_level'] = user[0].user_level
                return redirect(reverse('user_dashboard:dashboard'))
            else:
                messages.error(request, "Incorrect username or password")
                request.session['logged_in'] = False
            return redirect(reverse('user_dashboard:sign_in'))

def log_off(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect(reverse('user_dashboard:sign_in'))


def register(request):
    if request.method == "GET":
        context = {
            'messages' : messages.get_messages(request)
        }
        return render(request, 'user_dashboard/register.html', context)
    else:
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            messages.error(request, "There were errors validating input")
            print errors
            return redirect(reverse('user_dashboard:register'))
        errors = User.objects.user_exist_check(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, "That email is already taken")
            print errors
            return redirect(reverse('user_dashboard:register'))
        else:
            print "No errors validating"
            user = User.objects.user_add(request.POST)
            messages.success(request, "Successfully registered user")
            print user
            return redirect(reverse('user_dashboard:sign_in'))

def dashboard(request):
    if 'logged_in' not in request.session:
        messages.error(request, 'Not logged in')
        return redirect(reverse('user_dashboard:sign_in'))
    context = {
        'users' : User.objects.all()
    }
    return render(request, 'user_dashboard/dashboard.html', context)

def new_user(request):
    if request.method == "GET":
        return render(request, 'user_dashboard/new_user.html')
    else:
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            messages.error(request, "There were errors validating input")
            print errors
            return redirect(reverse('user_dashboard:new_user'))
        errors = User.objects.user_exist_check(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, "That email is already taken")
            print errors
            return redirect(reverse('user_dashboard:new_user'))
        else:
            print "No errors validating"
            user = User.objects.user_add(request.POST)
            messages.success(request, "Successfully registered user")
            print user
            return redirect(reverse('user_dashboard:new_user'))

def edit(request):
    if 'logged_in' not in request.session:
        messages.error(request, 'Not logged in')
        return redirect(reverse('user_dashboard:sign_in'))
    context = {
        'user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'user_dashboard/edit.html', context)

def edit_user_id(request, user_id):
    if 'logged_in' not in request.session:
        messages.error(request, 'Not logged in')
        return redirect(reverse('user_dashboard:sign_in'))
    if request.session['user_level'] != 9:
        messages.error(request, 'You do not have access to this page')
        return redirect(reverse('user_dashboard:dashboard'))

    context = {
        'user' : User.objects.get(id=user_id)
    }
    return render(request, 'user_dashboard/edit_user_id.html', context)

def destroy(request,user_id):
    print 'in destroy user'
    user = User.objects.get(id=user_id).delete()
    messages.success(request, 'Successfully deleted user')
    return redirect(reverse('user_dashboard:dashboard'))

def update(request):
    print "in update"
    user = User.objects.get(id=request.session['user_id'])
    print "got user:"
    email = request.POST['email']
    fn = request.POST['first_name']
    ln = request.POST['last_name']

    # validate post data
    errors = []
    if not re.match(EMAIL_REGEX, email):
        errors.append('Email is invalid')
    if len(fn) < 3 or len(ln) < 3:
        errors.append("First and Last name must be at least 3 characters in length")
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect(reverse('user_dashboard:edit_user'))

    if user.email.lower() != email.lower():
        print "attempting to change email"
        errors = User.objects.user_exist_check(request.POST)
        if len(errors) > 0:
            messages.error(request, "That email is already taken")
            return redirect(reverse('user_dashboard:edit_user'))
        else:
            print "That email is not taken"
            user.email = email
            user.first_name = fn
            user.last_name = ln
            user.save()
            messages.success(request, 'Successfully edited user information')
            return redirect(reverse('user_dashboard:edit_user'))
    else:
        user.email = email
        user.first_name = fn
        user.last_name = ln
        user.save()
    messages.success(request, 'Successfully edited user information')
    return redirect(reverse('user_dashboard:edit_user'))

def update_user_id(request, user_id):
    print "in update_user_id"

    user = User.objects.get(id=user_id)

    if user.email.lower() != request.POST['email'].lower():
        errors = User.objects.filter(email__iexact=request.POST['email'])
        if len(errors):
            messages.error(request, "Found another user with that email")
        else:
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            messages.success(request, "Successfully changed user's info!")
    else:
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        messages.success(request, "Successfully changed user's info!")
    return redirect(reverse('user_dashboard:edit_user_id', kwargs={'user_id':user_id}))

def update_password(request):
    errors = []
    if len(request.POST['password']) < 8:
        errors.append("Password must be at least 8 characters")
    if request.POST['password'] != request.POST['pw_conf']:
        errors.append("Passwords do not match")

    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect(reverse('user_dashboard:edit_user'))

    user = User.objects.get(id=request.session['user_id'])
    user.hash_pw = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt())
    user.save()
    messages.success(request, "Successfully updated password")
    return redirect(reverse('user_dashboard:edit_user'))

def update_password_id(request, user_id):
    print "in update_password_id"
    errors = []
    if len(request.POST['password']) < 8:
        errors.append("Password must be at least 8 characters")
    if request.POST['password'] != request.POST['pw_conf']:
        errors.append("Passwords do not match")

    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect(reverse('user_dashboard:edit_user_id', kwargs={'user_id':user_id}))

    user = User.objects.get(id=user_id)
    user.hash_pw = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt())
    user.save()
    messages.success(request, "Successfully updated password")
    return redirect(reverse('user_dashboard:edit_user_id', kwargs={'user_id':user_id}))

def update_desc(request):
    user = User.objects.get(id=request.session['user_id'])
    print "got user:" + str(user.first_name)
    print "user desc:" + str(user.desc)
    user.desc = request.POST['desc']
    user.save()
    messages.success(request, "Successfully updated user description")
    return redirect(reverse('user_dashboard:edit_user'))

def show(request, user_id):

    context = {
        'user' : User.objects.get(id=user_id),
        'now' : datetime.now(),
        'user_messages' : Message.objects.filter(message_to=user_id),
        'messages' : messages.get_messages(request),
        'comments' : Comment.objects.filter(id__in = Message.objects.filter(message_to=user_id).values('comment'))
    }
    return render(request, 'user_dashboard/user.html', context)

def message(request, user_id):

    user = User.objects.get(id=user_id)
    print "got user:" + str(user.first_name)

    if len(request.POST['message']) < 2:
        messages.error(request,'Message must be longer than 2 characters')
    else:
        Message.objects.create(message=request.POST['message'], message_to=user, message_by=User.objects.get(id=request.session['user_id']))
        messages.success(request, "Successfully posted message")
    return redirect(reverse('user_dashboard:show_user', kwargs={'user_id':user_id}))
    return redirect(reverse('user_dashboard:show_user', kwargs={'user_id':user_id}))

def comment(request, message_id):

    user = Message.objects.get(id=message_id).message_to.id
    if len(request.POST['comment']) < 2:
        messages.error(request, "Comment must be at least 2 characters in length")
    else:
        Comment.objects.create(comment=request.POST['comment'], comment_by=User.objects.get(id=request.session['user_id']), message = Message.objects.get(id=message_id))
        messages.success(request, "Successfully posted a comment")
    return redirect(reverse('user_dashboard:show_user', kwargs={'user_id' : user}))
