# -*- coding: utf-8 -*-
import datetime
import time
import os
from site_pet.settings import MEDIA_ROOT
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from members.models import Member
from .forms import *
from .models import Event, Spectator, Categoria
from django.utils import formats
import json
from django.core.mail import send_mail
from datetime import timezone
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request):
	try:
		member = get_object_or_404(Member, user=request.user)
	except:
		member = None
	nexteventsList = Event.objects.order_by('start_date').filter(start_date__gte=datetime.date.today())
	eventsList = Event.objects.all()
	events=[]
	for event in nexteventsList:
		date_start_correct = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.combine(event.start_date, event.beginTime))
		date_end_correct = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.combine(event.end_date, event.beginTime))
		events.append([date_start_correct, date_end_correct, event.name, '#5f5f7b', '/events/'+event.slug])
	return render(request, 'events/index.html', {'eventsList': nexteventsList, 'onlyFuture': True,'member':member, 'events': json.dumps(events)})

def addEvent(request):
	if request.method == 'POST':
		form = EventForm(request.POST)

		if form.is_valid():
			newEvent = Event()
			newEvent.name = form.cleaned_data['name']
			newEvent.start_date = form.cleaned_data['start_date']
			newEvent.end_date = form.cleaned_data['end_date']
			newEvent.beginTime = form.cleaned_data['beginTime']
			newEvent.endTime = form.cleaned_data['endTime']
			newEvent.address = form.cleaned_data['address']
			newEvent.description = form.cleaned_data['description']
			newEvent.slug = newEvent.unique_slug_generator()

			newEvent.save()
			messages.success(request, 'Evento criado com sucesso.')

			return redirect(reverse('events:event', args=(newEvent.slug,)))

		return render(request, 'blog/form.html', {'title':"Cadastrar um novo evento", 'form': form}, status=400)
	return render(request, 'blog/form.html', {'title':"Cadastrar um novo evento", 'form': EventForm()})

def editEvent(request, slug):
	event = get_object_or_404(Event, slug=slug)
	if request.method == 'POST':
		form = EventForm(request.POST)

		if form.is_valid():
			event.name = form.cleaned_data['name']
			event.slug = event.unique_slug_generator()
			event.start_date = form.cleaned_data['start_date']
			event.end_date = form.cleaned_data['end_date']
			event.beginTime = form.cleaned_data['beginTime']
			event.endTime = form.cleaned_data['endTime']
			event.address = form.cleaned_data['address']
			event.description = form.cleaned_data['description']

			event.save()
			messages.success(request, 'Alterações salvas com sucesso.')

			return redirect(reverse('events:event', args=(event.slug,)))

		return render(request, 'blog/form.html', {'title':"Editar a atividade: " + event.name, 'form': form}, status=400)

	return render(request, 'blog/form.html' , {'title':"Editar a atividade: " + event.name, 'form': EventForm(initial={'name':event.name, 'start_date':event.start_date, 'end_date':event.end_date, 'address':event.address, 'beginTime':event.beginTime, 'endTime':event.endTime, 'description':event.description, })})

def event(request, slug):
	event = get_object_or_404(Event, slug=slug)
	confirmed = Spectator.objects.order_by('date').filter(event=event, confirmed=True)
	tipo_evento=dict(Event.TIPO_EVENTO)[event.tipo]
	if "http" not in event.link: 
		event.link="http://"+event.link
	#gmaps = GoogleMaps(API_KEY)
	#lat, lng = gmaps.address_to_latlng(event.address)
	if request.method == 'POST':
		if request.POST['delete']:
			for spectator in Spectator.objects.filter(event=event):
				spectator.delete()
			event.delete()
			return HttpResponseRedirect(reverse('events:index'))
		else:
			return render(request, 'events/event.html', {'event': event, 'confirmed': confirmed, 'error_message': "Erro ao deletar evento",'tipo_evento':tipo_evento,})
	else:
		return render(request, 'events/event.html', {'event': event, 'confirmed': confirmed,'tipo_evento':tipo_evento,})

def allEvents(request):
	eventsList = Event.objects.order_by('start_date')
	try:
		member = get_object_or_404(Member, user=request.user)
	except:
		member = None
	nexteventsList = Event.objects.order_by('start_date').filter(start_date__gte=datetime.date.today())
	eventsList = Event.objects.all()
	events=[]
	for event in eventsList:
		date_start_correct = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.combine(event.start_date, event.beginTime))
		date_end_correct = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.combine(event.end_date, event.beginTime))
		events.append([date_start_correct, date_end_correct, event.name, '#5f5f7b', '/events/'+event.slug])
	return render(request, 'events/index.html', {'eventsList': eventsList, 'onlyFuture': False, 'member':member, 'events': json.dumps(events)})

def subscribe(request, slug):
	event = get_object_or_404(Event, slug=slug)
	now = datetime.date.today()

	if now >= event.start_date:
		messages.error(request, "Inscrições encerradas para " + str(event.name))
		return redirect(reverse('events:event', args=(event.slug,)))

	if request.method == 'POST':
		form = SpectatorForm(request.POST)

		if form.is_valid():
			newSpectator = Spectator()
			newSpectator.name = form.cleaned_data['name']
			newSpectator.email = form.cleaned_data['email']
			newSpectator.cpf = form.cleaned_data['cpf']
			if form.cleaned_data['isFromCEFET'] == True:
				newSpectator.confirmed = True
				newSpectator.enrollNum = form.cleaned_data['enrollNum']
			newSpectator.isFromCEFET = form.cleaned_data['isFromCEFET']
			newSpectator.occupation = form.cleaned_data['occupation']
			newSpectator.event = event

			newSpectator.save()

			messages.success(request, 'Inscrição realizada com sucesso.')

			if newSpectator.confirmed == True:
				subject = "Cadastro aprovado na atividade: " + newSpectator.event.name
				message = "Olá, o PET de Engenharia de Computação do CEFET-MG BH (COMPET) informa que o seu cadastro na atividade: \"" + newSpectator.event.name + "\" foi aceito, esperamos sua participação na data " + Event.dateString(newSpectator.event) + ".\n\n Obrigado!\n\n--\nMensagem enviada automaticamente."
				try:
					send_mail(subject, message, 'grupo.compet@gmail.com', [newSpectator.email])
				except:
					print('Erro')
			return redirect(reverse('events:event', args=(event.slug,)))

		return render(request, 'blog/form.html', {'title':"Realizar nova inscrição", 'form': form}, status=400)
	else:
		if request.user.is_authenticated :
			member = Member.objects.filter(user=request.user).first()
			if member:
				return render(request, 'blog/form.html', {'title':"Cadastrar um novo evento", 'form': SpectatorForm(initial={'name':member.name,
				'email': member.email, 'isFromCEFET': True, 'occupation': str(member.role)+ " do PET de " + str(member.pet)})})
			else:
				return render(request, 'blog/form.html', {'title':"Cadastrar um novo evento", 'form': SpectatorForm()})
	return render(request, 'blog/form.html', {'title':"Realizar nova inscrição", 'form': SpectatorForm()})

def pending(request):
	pendingList = Spectator.objects.order_by('date').filter(confirmed=False)
	return render(request, 'events/pending.html', {'pendingList': pendingList})

def pendingAutorize(request, id, slug):
	event = Event.objects.filter(slug=slug).first()
	spec = get_object_or_404(Spectator, id=id)
	if event:
		spec.confirmed = True
		spec.save()

	return redirect(reverse('events:pending'))

def pendingRemove(request, id, slug):
	event = Event.objects.filter(slug=slug).first()
	spec = get_object_or_404(Spectator, id=id)
	if event:
		if spec.confirmed:
			spec.confirmed=False
			spec.save()
		else:
			spec.delete()

	return redirect(reverse('events:pending'))

def generateCertificates(request, slug):

	event = Event.objects.filter(slug=slug).first()
	spectators = Spectator.objects.filter(confirmed=True, event=event)

	#Query.all.fitler(username=username)


	mes_ext = {1: 'Janeiro', 2 : 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio',6:'Junho',7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'}
	width=3507;
	height=2480;

	data=time.strftime("%d")
	data+=" de "
	data+=mes_ext[int(time.strftime("%m"))]
	data+=" de "
	data+=time.strftime("%Y")

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="Certificados.pdf"'
	pdf = canvas.Canvas(response, (width,height));

	for spec in spectators:
		pdf.drawImage('static/media/Certificado.jpg',0,0,width,height)
		pdf.setFont('Helvetica',80, leading=None)
		pdf.drawCentredString(1750,1450,"Certicamos que ")
		pdf.setFont('Helvetica-Bold',80, leading=None)
		pdf.drawCentredString(1750,1350, spec.name)
		pdf.setFont('Helvetica',80, leading=None)
		pdf.drawCentredString(1750,1250,"participou do "+event.name)
		pdf.drawCentredString(1750,1150,"no "+event.address)

		if event.start_date != event.end_date:
			if (event.end_date.day - event.start_date.day) < 2:
				pdf.drawCentredString(1750,1050,"em "+str(event.start_date.day)+" e "+ str(event.end_date.day) +" de "+ mes_ext[event.start_date.month]+" de "+str(event.start_date.year)+ " das "+str(event.beginTime)+" às "+str(event.endTime))
			else:
				if event.end_date.year != event.start_date.year:
					pdf.drawCentredString(1750,1050,"em "+str(event.start_date.day)+" de "+ mes_ext[event.start_date.month]+" de "+str(event.start_date.year)+" a " + str(event.end_date.day)+" de "+ mes_ext[event.end_date.month]+" de "+str(event.end_date.year)+" das "+str(event.beginTime)+" às "+str(event.endTime))
				else:
					pdf.drawCentredString(1750,1050,"de "+str(event.start_date.day)+" a "+ str(event.end_date.day) +" de "+ mes_ext[event.start_date.month]+" de "+str(event.start_date.year)+ " das "+str(event.beginTime)+" às "+str(event.endTime))
		else:
			pdf.drawCentredString(1750,1050,"em "+str(event.start_date.day)+" de "+ mes_ext[event.start_date.month]+" de "+str(event.start_date.year)+ " das "+str(event.beginTime)+" às "+str(event.endTime))


		pdf.drawCentredString(840,700,"Belo Horizonte, "+ data)
		pdf.showPage()
	pdf.save()
	
	return response

def viewcats(request):
	catsList = Categoria.objects.order_by('name')
	return render(request, 'events/tag.html')

