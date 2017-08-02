# -*- coding: utf-8 -*-
import datetime

from django.db import models

class Event(models.Model):

	name = models.CharField(max_length=80)
	description = models.CharField(max_length=1000)
	address = models.CharField(max_length=250)
	date = models.DateField('Data do evento')
	# time = models.TimeField('Hora do evento', default=datetime.time(00,00))
	beginTime = models.TimeField('Horário de início do evento', default=None, blank=True, null=True)
	endTime = models.TimeField('Horário de término do evento', default=None, blank=True, null=True)

	# confirmed = []

	def __str__(self):
		return self.name

class Spectator(models.Model):

	name = models.CharField(max_length=100)
	email = models.EmailField()
	cpf = models.CharField(max_length=11)
	isFromCEFET = models.BooleanField(default=False)
	occupation = models.CharField(max_length=80)
	enrollNum = models.CharField(max_length=12, default=None, blank=True, null=True) # matrícula

	date = models.DateTimeField('Momento da inscrição', auto_now=True)
	confirmed = models.BooleanField(default=False)

	event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)

	def __str__(self):
		return self.name + ' em ' + self.event.name
