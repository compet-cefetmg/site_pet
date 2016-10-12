from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='blog.index'),
    url(r'^publication/(?P<id>[0-9]+)$', views.show, name='blog.show'),
]
