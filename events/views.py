# -*- coding: utf-8 -*-
import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import *
from .models import Event, Spectator

def addEvent(request):
	if request.method == 'POST':
		try:
			newEvent = Event()
			newEvent.name = request.POST['name']
			newEvent.date = request.POST['date']
			if request.POST['beginTime']:
				newEvent.beginTime = request.POST['beginTime']
			if request.POST['endTime']:
				newEvent.endTime = request.POST['endTime']
			newEvent.address = request.POST['address']
			newEvent.description = request.POST['description']
		except:
			return render(request, 'events/add.html', {'error_message': "Erro ao criar evento",})
		else:
			newEvent.save()
			return HttpResponseRedirect(reverse('events:event', args=(newEvent.name,)))
	return render(request, 'events/add.html', {'form': EventForm()})	
	# else:
	# 		return render(request, 'events/add.html')
	# if request.method == 'POST':

def editEvent(request, name):
	event = get_object_or_404(Event, name=name)
	if request.method == 'POST':
		try:
			if request.POST['name']:
				event.name = request.POST['name']
			if request.POST['date']:
				event.date = request.POST['date']
			if request.POST['beginTime']:
				event.beginTime = request.POST['beginTime']
			if request.POST['endTime']:
				event.endTime = request.POST['endTime']
			if request.POST['address']:
				event.address = request.POST['address']
			if request.POST['description']:
				event.description = request.POST['description']
		except:
			return render(request, 'events/edit.html', {'event': event, 'error_message': "Erro ao editar evento",})
		else:
			event.save()
			return HttpResponseRedirect(reverse('events:event', args=(event.name,)))
	else:
		return render(request, 'events/edit.html', {'event': event})

def event(request, name):
	event = get_object_or_404(Event, name=name)
	confirmed = Spectator.objects.order_by('date').filter(event=event).filter(confirmed=True)
	if request.method == 'POST':
		if request.POST['delete']:
			event.delete()
			return HttpResponseRedirect(reverse('events:index'))
		else:
			return render(request, 'events/event.html', {'event': event, 'confirmed': confirmed, 'error_message': "Erro ao deletar evento",})
	else:
		return render(request, 'events/event.html', {'event': event, 'confirmed': confirmed,})

def index(request):
	eventsList = Event.objects.order_by('date').filter(date__gte=datetime.date.today())
	return render(request, 'events/index.html', {'eventsList': eventsList, 'onlyFuture': True,})

def allEvents(request):
	eventsList = Event.objects.order_by('date')
	return render(request, 'events/index.html', {'eventsList': eventsList})

def subscribe(request, name):
	event = get_object_or_404(Event, name=name)
	if request.method == 'POST':
		try:
			newSpectator = Spectator()
			newSpectator.name = request.POST['name']
			newSpectator.email = request.POST['email']
			newSpectator.cpf = request.POST['cpf']
			if 'fromCEFET' in request.POST:
				newSpectator.isFromCEFET = True
				newSpectator.confirmed = True
				newSpectator.enrollNum = request.POST['enrollNum']
			newSpectator.occupation = request.POST['occupation']
			newSpectator.event = event
		except:
			return render(request, 'events/subscribe.html', {'event': event, 'error_message': "Erro ao realizar inscrição",})
		else:
			newSpectator.save()
			return HttpResponseRedirect(reverse('events:event', args=(event.name,)))
	else:
		return render(request, 'events/subscribe.html', {'event': event})

def pending(request):
	pendingList = Spectator.objects.order_by('date').filter(confirmed=False)
	if request.method == 'POST':
		try:
			checkedList = request.POST.getlist('selected')
			if 'approve' in request.POST:
				for spectator in pendingList:
					if str(spectator) in checkedList:
						spectator.confirmed = True
						spectator.save()
			if 'exclude' in request.POST:
				for spectator in pendingList:
					if str(spectator) in checkedList:
						spectator.delete()
		except:
			return render(request, 'events/pending.html', {'pendingList': pendingList, 'error_message': "Erro ao lidar com as inscrições",})
		else:
			# return HttpResponseRedirect(reverse('events:index'))
			return HttpResponseRedirect(reverse('events:pending'))
	else:
		return render(request, 'events/pending.html', {'pendingList': pendingList})

def pendingSpecific(request, name):
	event = get_object_or_404(Event, name=name)
	if event:
		pendingList = Spectator.objects.order_by('date').filter(confirmed=False).filter(event=event)
		if request.method == 'POST':
			try:
				checkedList = request.POST.getlist('selected')
				if 'approve' in request.POST:
					for spectator in pendingList:
						if str(spectator) in checkedList:
							spectator.confirmed = True
							spectator.save()
				if 'exclude' in request.POST:
					for spectator in pendingList:
						if str(spectator) in checkedList:
							spectator.delete()
			except:
				return render(request, 'events/pending.html', {'pendingList': pendingList, 'error_message': "Erro ao lidar com as inscrições", 'event': event,})
			else:
				# return HttpResponseRedirect(reverse('events:event', args=(event.name,)))
				return HttpResponseRedirect(reverse('events:pendingSpecific', args=(event.name,)))
	return render(request, 'events/pending.html', {'pendingList': pendingList, 'event': event})
