from django.conf.urls import url
from members import views

urlpatterns = [
    url(r'^$', views.index, name='members.index'),
    url(r'^member/add/$', views.add_member, name='members.add_member'),
    url(r'^edit/me/$', views.edit_personal_info, name='members.edit_personal_info'),
]
