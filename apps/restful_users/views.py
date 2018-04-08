from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import *

# Create your views here.
def index(request):
    print "in restful index"
    context = {
        'users' : User.objects.all()
    }
    return render(request, 'restful_users/index.html', context)

def new_user(request):
    if request.method == "POST":
        print "*"*50
        print "method was post"
        print request.POST['first_name']
        print request.POST['last_name']
        print request.POST['email']
        errors = User.objects.basic_validator(request.POST)
        print errors
        if len(errors):
            for key in errors:
                request.session[key] = errors[key]
            print "there were errors on validate"
            return redirect(reverse('new_user'))
        errors = User.objects.user_exist_check(request.POST)
        print errors
        print type(errors)
        if len(errors):
            myErrors = []
            for key in errors:
                myErrors.append(errors[key])
            request.session['errors'] = myErrors
            print "there were errors on user check"
            return redirect(reverse('new_user'))
        request.session.pop('errors')
        User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'])
        print "*"*50

        return redirect(reverse('restful_index'))
    else:
        return render(request, 'restful_users/new_user.html')

def show(request, user_id):
    return render(request, 'restful_users/user.html', context = {'user':User.objects.get(id=user_id)})

def edit(request, user_id):
    return render(request, 'restful_users/edit.html', context = {'user':User.objects.get(id=user_id)})

def update(request):
    user_id = request.POST['user_id']
    user = User.objects.get(id=user_id)
    errors = User.objects.basic_validator(request.POST)
    print errors
    if len(errors):
        myErrors = []
        for key in errors:
            myErrors.append(errors[key])
        request.session['errors'] = myErrors
        print "there were errors on validate"
        return redirect(reverse('edit_user', kwargs={user_id:user_id}))
    if user.email != request.POST['email']:
        errors = User.objects.user_exist_check(request.POST)
        if len(errors):
            myErrors = []
            for key in errors:
                myErrors.append(errors[key])
            request.session['errors'] = myErrors
            print "there were errors on user check"
            return redirect(reverse('edit_user', kwargs={'user_id':user_id}))
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect(reverse('restful_index'))

def destroy(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect(reverse('restful_index'))
