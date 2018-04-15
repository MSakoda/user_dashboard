from django.conf.urls import url
from . import views
from models import *

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^signout$', views.signout, name='signout'),
    url(r'^register$', views.register, name='register'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^events/new$', views.create_event, name='create_event'),
    url(r'^events/show/(?P<event_id>\d+)$', views.show_event, name='event'),
    url(r'^users/update$', views.update_user, name='update_user'),
    url(r'^users/password/update$', views.update_password, name='update_password'),
    url(r'^users/friends$', views.friends, name='friends'),
]
