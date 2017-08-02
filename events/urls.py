from django.conf.urls import url
from . import views

app_name = 'events'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^all/$', views.allEvents, name='allEvents'),
	url(r'^add/$', views.addEvent, name='add'),
	url(r'^pending/$', views.pending, name='pending'),
	url(r'^pending/(?P<name>[A-Za-z0-9]+)/$', views.pendingSpecific, name='pendingSpecific'),
	url(r'^(?P<name>[A-Za-z0-9]+)/$', views.event, name='event'),
	url(r'^(?P<name>[A-Za-z0-9]+)/edit/$', views.editEvent, name='edit'),
    url(r'^(?P<name>[A-Za-z0-9]+)/subscribe/$', views.subscribe, name='subscribe'),
]
