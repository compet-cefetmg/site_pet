from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<username>[a-zA-Z0-9]+)$', views.index),
    url(r'^publication/(?P<id>[0-9]+)$', views.show, name='blog.show'),
]
