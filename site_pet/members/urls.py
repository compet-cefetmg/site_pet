from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='members.index'),
    url(r'^member/add/$', views.add_member, name='members.add_member'),
    url(r'^tutor/add/$', views.add_tutor, name='members.add_tutor'),
    url(r'^tutor/all/$', views.all_tutors, name='members.all_tutors'),
    url(r'^member/all/$', views.all_members, name='members.all_members'),
    url(r'^member/edit/$', views.edit_member, name='members.edit_member'),
    url(r'^[A-Za-z0-9]*/edit/$', views.edit_member_role, name='members.edit_member_role'),
]
