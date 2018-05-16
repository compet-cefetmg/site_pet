# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.template.defaultfilters import slugify
import random
import string
from django.utils import formats

class Categoria(models.Model):
	name = models.CharField(max_length=100,unique=True)
	descricaocurta = models.CharField(max_length=300)
	frequencia = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Event(models.Model):
	TIPO_EVENTO = [
        ('EN', 'Ensino'),
        ('EX', 'Extensão'),
        ('PE', 'Pesquisa'),
    ]

	name = models.CharField(max_length=80)
	slug = models.SlugField(null=True, blank=True, unique=True)
	
	tipo= models.CharField(max_length=2,default='EN',choices=TIPO_EVENTO)
	link = models.CharField(max_length=100)
	tags = models.ManyToManyField(Categoria)

	description = models.CharField(max_length=5000)
	cronograma = models.CharField(max_length=5000)

	address = models.CharField(max_length=250)
	start_date = models.DateField('Data de início do evento')
	end_date = models.DateField('Data de término do evento')
	
	beginTime = models.TimeField('Horário de início do evento', default=None, blank=True, null=True)
	endTime = models.TimeField('Horário de término do evento', default=None, blank=True, null=True)

	def __str__(self):
		return str(self.name) + ' - ' + str(self.start_date)


	def unique_slug_generator(self, new_slug=None):
		DONT_USE=['all', 'add', 'pending']
		if new_slug is not None:
			slug = new_slug
		else:
			slug = slugify(self.name)
		if slug in DONT_USE:
			new_slug = "{slug}-{randstr}".format(
				slug=slug,
				randstr=''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(4))
			)
			return self.unique_slug_generator(new_slug=new_slug)
		Klass = self.__class__
		qs_exists = Klass.objects.filter(slug=slug).exists()
		if qs_exists:
			new_slug = "{slug}-{randstr}".format(
				slug=slug,
				randstr=''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(4))
			)
			return self.unique_slug_generator(new_slug=new_slug)
		return slug
	# confirmed = []

	def dateString(self):
		return str(self.start_date.day) + '/' + str(self.start_date.month) + '/' + str(self.start_date.year)

class Spectator(models.Model):

	name = models.CharField(max_length=100)
	email = models.EmailField()
	cpf = models.CharField(max_length=14)
	isFromCEFET = models.BooleanField(default=False)
	occupation = models.CharField(max_length=80)
	enrollNum = models.CharField(max_length=12, default=None, blank=True, null=True) # matrícula

	date = models.DateTimeField('Momento da inscrição', auto_now=True)
	confirmed = models.BooleanField(default=False)

	event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)

	def __str__(self):
		return self.name + ' em ' + self.event.name
