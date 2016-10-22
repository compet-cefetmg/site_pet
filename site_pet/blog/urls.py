from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.index, name='blog.index'),
    url(r'^post/(?P<id>\d+)/$', views.post, name='blog.post'),
]
