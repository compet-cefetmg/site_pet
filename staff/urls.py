from django.conf.urls import url
from staff import views

urlpatterns = [
    url(r'^$', views.index, name='staff.index'),
    url(r'^permission/(?P<id>\d+)/(?P<autorize>\w+)/$', views.autorize_member, name='staff.autorize_member'),
    url(r'^delete/(?P<id>\d+)/$', views.delete_member, name='staff.delete_member'),
    url(r'^login$', views.auth_login, name='staff.auth_login'),
    url(r'^logout$', views.auth_logout, name='staff.auth_logout'),
]
