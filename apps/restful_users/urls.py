from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='restful_index'),
    url(r'^users/new$', views.new_user, name='new_user'),
    url(r'^users/(?P<user_id>\d+)$', views.show, name='show_user'),
    url(r'^users/(?P<user_id>\d+)/edit$', views.edit, name='edit_user'),
    url(r'^users/update$', views.update, name='update_user'),
    url(r'^users/(?P<user_id>\d+)/destroy$', views.destroy, name='destroy_user'),
]
