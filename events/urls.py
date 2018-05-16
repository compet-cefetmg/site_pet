from django.conf.urls import url
from . import views

app_name = 'events'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^all/$', views.allEvents, name='allEvents'),
	url(r'^add/$', views.addEvent, name='add'),
	url(r'^pending/$', views.pending, name='pending'),
	url(r'^viewtags/$', views.viewcats, name='viewtags'),
	url(r'^pendingAutorize/(?P<id>[0-9]+)/(?P<slug>[A-Za-z0-9-]+)/$', views.pendingAutorize, name='pendingAutorize'),
	url(r'^pendingRemove/(?P<id>[0-9]+)/(?P<slug>[A-Za-z0-9-]+)/$', views.pendingRemove, name='pendingRemove'),
	url(r'^(?P<slug>[A-Za-z0-9-]+)/$', views.event, name='event'),
	url(r'^(?P<slug>[A-Za-z0-9-]+)/edit/$', views.editEvent, name='edit'),
    url(r'^(?P<slug>[A-Za-z0-9-]+)/subscribe/$', views.subscribe, name='subscribe'),
	url(r'^(?P<slug>[A-Za-z0-9-]+)/certificado/$', views.generateCertificates, name='generateCertificates'),

]
