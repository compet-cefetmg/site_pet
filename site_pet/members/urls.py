from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='members.index'),
    url(r'^add/$', views.add_member, name='members.add_member'),
]
