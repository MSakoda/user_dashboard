from django.conf.urls import url
from . import views
from models import *

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.signin, name = 'sign_in'),
    url(r'^logoff$', views.log_off, name = 'log_off'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^dashboard$', views.dashboard, name = 'dashboard'),
    url(r'^users/edit$', views.edit, name = 'edit_user'),
    url(r'^users/new$', views.new_user, name = 'new_user'),
    url(r'^users/destroy/(?P<user_id>\d+)$', views.destroy, name = 'destroy_user'),
    url(r'^users/edit/(?P<user_id>\d+)$', views.edit_user_id, name = 'edit_user_id'),
    url(r'^users/(?P<user_id>\d+)/show$', views.show, name = 'show_user'),
    url(r'^users/update/$', views.update, name = 'update_user'),
    url(r'^users/update/(?P<user_id>\d+)$', views.update_user_id, name = 'update_user_id'),
    url(r'^users/update_password$', views.update_password, name = 'update_password'),
    url(r'^users/update_password/(?P<user_id>\d+)$', views.update_password_id, name = 'update_password_id'),
    url(r'^users/update_desc$', views.update_desc, name = 'update_desc'),
    url(r'^users/(?P<user_id>\d+)/message$', views.message, name='message'),
    url(r'^users/(?P<message_id>\d+)/comment$', views.comment, name='comment'),
]
