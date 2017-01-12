from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.index, name='blog.index'),
    url(r'^post/(?P<id>\d+)/$', views.post, name='blog.post'),
    url(r'^post/add/$', views.add_post, name='blog.add_post'),
    url(r'^post/all/$', views.all, name='blog.all'),
]
