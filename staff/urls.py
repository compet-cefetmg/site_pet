from django.conf.urls import url
from staff import views

urlpatterns = [
    url(r'^$', views.index, name='staff.index'),
    url(r'^login$', views.auth_login, name='staff.auth_login'),
    url(r'^logout$', views.auth_logout, name='staff.auth_logout'),
    url(r'^message$', views.send_admin_message, name='staff.send_admin_message'),
]
