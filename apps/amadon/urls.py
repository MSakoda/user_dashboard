from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^/test$', views.test),
    url(r'^(?P<number>\d+)$', views.buy, name='buy'),
    url(r'^checkout$', views.checkout),
]
