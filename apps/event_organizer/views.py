from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from datetime import datetime
import bcrypt

import re

from models import *

EMAIL_REGEX = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'


# Create your views here.
def index(request):
    return render(request, 'event_organizer/index.html')

def signin(request):

    # RENDER TEMPLATE
    if request.method == 'GET':
        return render(request, 'event_organizer/signin.html')

    # look for user by email
    else:
        user = User.objects.filter(email__iexact=request.POST['email'])

        # found user
        if len(user) > 0:

            hash_pw = user[0].hashpw

            # if password is correct
            if bcrypt.checkpw(request.POST['password'].encode(), hash_pw.encode()):
                messages.success(request, "Successfully logged in as {}".format(user[0].email))
                request.session['logged_in'] = True
                request.session['user_id'] = user[0].id
                return redirect(reverse('events:dashboard'))

            # Incorrect password
            else:
                messages.error(request, "Incorrect password")

        # did not find user
        else:
            messages.error(request, "did not find email in database")

        return redirect(reverse('events:signin'))

def signout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect(reverse('events:signin'))


def register(request):

    # RENDER PAGE
    if request.method == "GET":
        return render(request, 'event_organizer/register.html')

    # POST REQUEST
    else:
        errors = []
        # validate email
        if not re.match(EMAIL_REGEX, request.POST['email']):
            errors.append("Email is invalid")

        # validate password
        if len(request.POST['password']) < 8:
            errors.append('Password must be at least 8 characters in length')
        if request.POST['pw_conf'] != request.POST['password']:
            errors.append("Passwords do not match")

        #  flash error messages
        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)


        # make first user an admin
        if len(User.objects.all()) < 1:
            User.objects.create(email = request.POST['email'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], hashpw = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt()), user_level = 9)

        # any other user is regular ( user_level =1 )
        else:
            user = User.objects.filter(email__iexact = request.POST['email'])
            if len(user) > 0:
                messages.error(request, 'User already exists in database')
                return redirect(reverse('events:register'))
            else:
                User.objects.create(email = request.POST['email'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], hashpw = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt()))

        messages.success(request, "Successfully created user: {}".format(request.POST['email']))
        return redirect(reverse('events:register'))

def profile(request):
    if not check_login(request):\
        return redirect(reverse('events:signin'))

    context = {
        'user' : User.objects.get(id=request.session['user_id']),
        'states' : states
    }

    # if address exists for user, pass it
    if len(User.objects.filter(id=request.session['user_id'])[0].address.values()) > 0:
        context['address'] = User.objects.filter(id=request.session['user_id'])[0].address.values()[0]

    return render(request, 'event_organizer/profile.html', context)

def update_user(request):

    # make sure required inputs are met
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    # phone is optional
    phone = request.POST['phone']

    # if any part of address is filled
    # require all fields to be present
    address = {
        'street' : request.POST['street'],
        'street2' : request.POST['street2'],
        'city' : request.POST['city'],
        'state' : request.POST['state'],
        'zipcode' : request.POST['zipcode']
    }

    hasAddress = False
    for key in address:
        if address[key] != '':
            hasAddress = True

    hasErrors = False
    #  get user
    user = User.objects.get(id=request.session['user_id'])

    # check if email is different
    if user.email.lower() != email.lower():
        # if different, make sure it's not already taken
        errors = User.objects.filter(email__iexact = email)
        if len(errors):
            messages.error(request, "That email already exists")
        hasErrors = True

    # if any errors, don't create user
    if hasErrors:
        return redirect(reverse("events:profile"))

    # create user
    else:

        if hasAddress == True:

            # check if any address connected to this user
            address_obj = Address.objects.filter(user=user)

            print "address_obj:"
            print address_obj.values()
            print "length:"
            print len(address_obj)
            # it exists, update it with this data
            if len(address_obj) > 0:
                address_obj[0].street = request.POST['street']
                address_obj[0].street2 = request.POST['street2']
                address_obj[0].city = request.POST['city']
                address_obj[0].state = request.POST['state']
                address_obj[0].zipcode = request.POST['zipcode']
                address_obj[0].save()
            # it doesn't exist, so create new address
            else:
                address_obj = Address.objects.create(street = request.POST['street'], street2 = request.POST['street2'], city = address['city'], state = address['state'], zipcode = address['zipcode'])
                print "address obj:"
                print address_obj
                address_obj.user = user
                address_obj.save()
                messages.success(request,'Did not find address: creating one')
        else:
            # remove address
            user.address.remove()


        user.phone = phone
        user.save()
        messages.success(request, "Successfully updated user")
        return redirect(reverse("events:profile"))

def update_password(request):

    password = request.POST['password']
    pw_conf = request.POST['pw_conf']

    errors = False

    if len(password) < 8:
        messages.error(request, "Password must be at least 8 characters in length")
        errors = True
    if password != pw_conf:
        messages.error(request, "Passwords do not match")
        errors = True

    if errors:
        return redirect(reverse("events:profile"))
    else:
        user = User.objects.get(id=request.session['user_id'])
        user.hashpw = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt() )
        user.save()
        messages.success(request, "Successfully updated password")

    return redirect(reverse("events:profile"))

def dashboard(request):
    # check if logged in
    if not check_login(request):
        return redirect(reverse('events:signin'))
    # else:
    #     return render(request, 'event_organizer/dashboard.html')
    context = {
        'events' : Event.objects.filter(created_by_user=request.session['user_id'])
    }
    return render(request, 'event_organizer/dashboard.html', context)

def create_event(request):
    if check_login(request) == False:
        return redirect(reverse('events:login'))
    else:
        context = {
            'states' : states
        }
        if request.method == "GET":
            return render(request, 'event_organizer/create_event.html', context)
        else:
            formVals = {
                'date' : request.POST['date'],
                'num_guests' : request.POST['num_guests'],
                'start_time' : request.POST['start_time'],
                'end_time' : request.POST['end_time'],
                'number_of_artists' : request.POST['number_of_artists'],
                'desc' : request.POST['desc'],
                'indoor_outdoor' : request.POST['indoor_outdoor'],
                'digital_traditional' : request.POST['digital_traditional'],
                'custom_border' : request.POST['custom_border'],
                'parking_info' : request.POST['parking_info'],
                'contact_name' : request.POST['contact_name'],
                'company' : request.POST['company'],
                'phone' : request.POST['contact_phone'],
                'email' : request.POST['contact_email'],
                'street' : request.POST['street'],
                'street2' : request.POST['street2'],
                'city' : request.POST['city'],
                'state' : request.POST['state'],
                'zipcode' : request.POST['zipcode']
            }
            print formVals


            # create client object, store as variable to reference later
            contact = Contact.objects.create(full_name = formVals['contact_name'], phone = formVals['phone'], email = formVals['email'])

            # create address object, store as variable to reference later
            address = Address.objects.create(street=formVals['street'], street2=formVals['street2'], city=formVals['city'], state=formVals['state'], zipcode=formVals['zipcode'])

            indoor = False
            digital = False
            if formVals['indoor_outdoor'] == 'indoor':
                indoor = True

            if formVals['digital_traditional'] == 'digital':
                digital = True

            # create event object and attach client and address and user
            event = Event.objects.create(
                created_by_user = User.objects.get(id=request.session['user_id']),
                indoor = indoor,
                digital = digital,
                number_of_artists = formVals['number_of_artists'],
                number_of_guests = formVals['num_guests'],
                address = address,
                contact = contact,
                date = formVals['date'],
                start_time = formVals['start_time'],
                end_time = formVals['end_time'],
                parking_info = formVals['parking_info'],
                border_inquiry = formVals['custom_border'],
                desc = formVals['desc'],
            )

            print "event:"
            print event

            messages.success(request, "Successfully created an event")
            return redirect(reverse('events:create_event'))

def show_event(request,event_id):
    if check_login(request) == False:
        return redirect(reverse('events:login'))
    else:
        print "showing event_id: {}".format(event_id)
        context = {
            'event' : Event.objects.get(id=event_id)
        }
        return render(request, 'event_organizer/event.html', context)

def friends(request):
    if check_login(request) == False:
        return redirect(reverse('events:login'))
    else:
        return render(request, 'event_organizer/friends.html')

# logs user out if not logged in
def check_login(request):
    if 'logged_in' not in request.session.keys():
        messages.error(request, 'Not logged in!!')
        return False
    else:
        return True

states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District Of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
