# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.db import models
from django.forms import ModelForm, Form
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django_summernote.widgets import SummernoteWidget
from .models import Event, Spectator, Categoria

class EventForm(forms.Form):

	name = forms.CharField(label='Nome do evento', widget=forms.TextInput(attrs={'class': 'form-control'}))

	tipo = forms.ChoiceField(label='Tipo do evento', required=True, choices=Event.TIPO_EVENTO)

	link = forms.CharField(label='Link do evento', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

	description = forms.CharField(label='Descrição', required=False, widget=SummernoteWidget())

	cronograma = forms.CharField(label='Cronograma', required=False, widget=SummernoteWidget())

	tags = forms.ModelMultipleChoiceField(label='Categorias', required=False, queryset=Categoria.objects.all())

	address = forms.CharField(label='Local', widget=forms.TextInput(attrs={'class': 'form-control'}))

	start_date = forms.DateField(label='Data de início', widget=forms.DateInput(attrs={'class': 'datepicker'}))

	end_date = forms.DateField(label='Data de término', widget=forms.DateInput(attrs={'class': 'datepicker'}))

	beginTime = forms.TimeField(label='Horário de início', widget=forms.TimeInput(attrs={'class':'timepicker'}))

	endTime = forms.TimeField(label='Horário de término', widget=forms.TimeInput(attrs={'class':'timepicker'}))

	def clean_name(self):
		data = self.cleaned_data['name']
		if len(data) > 80:
			raise ValidationError('Nome muito longo')
		return data

	def clean_description(self):
		data = self.cleaned_data['description']
		if len(data) > 1000:
			raise ValidationError('Descrição muito longa')
		return data

	def clean_address(self):
		data = self.cleaned_data['address']
		if len(data) > 250:
			raise ValidationError('Endereço muito longo')
		return data

	def clean_end_date(self):
		if self.cleaned_data['end_date'] and not self.cleaned_data['start_date']:
			raise ValidationError('Você não pode definir uma data de término sem definir uma data de começo.')
		if self.cleaned_data['end_date'] and self.cleaned_data['end_date'] < self.cleaned_data['start_date']:
			raise ValidationError('Data de término é anterior a data de começo.')
		return self.cleaned_data['end_date']# Não permite registrar data de saída sem a existência de uma data de entrada e não permite uma data de saída anterior a de entrada


class SpectatorForm(forms.Form):

	name = forms.CharField(label='Nome completo', widget=forms.TextInput(attrs={'class': 'form-control'}))

	email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'class': 'contatct-form'}))

	cpf = forms.CharField(label='CPF', widget=forms.TextInput(attrs={'class': 'cpfInput'}))

	isFromCEFET = forms.BooleanField(required=False, label='Você faz parte do CEFET?', widget=forms.RadioSelect(choices=[(True, 'Sim'), (False, 'Não')]))

	occupation = forms.CharField(required=False, label='Ocupação', widget=forms.TextInput(attrs={'class': 'form-control'}))

	enrollNum = forms.CharField(required=False, label='Número de matrícula (para alunos do CEFET)', widget=forms.TextInput(attrs={'class': 'matricula'})) # matrícula

	def clean_name(self):
		data = self.cleaned_data['name']
		if len(data) > 100:
			raise ValidationError('Nome muito longo')
		return data

	def clean_cpf(self):
		data = self.cleaned_data['cpf']
		if len(data) < 14:
			raise ValidationError('CPF muito curto')
		# if User.objects.filter(cpf=data).filter().exists():
            # raise ValidationError('Você já está cadastrado no evento')
		return data

	def clean_occupation(self):
		data = self.cleaned_data['occupation']
		if len(data) > 80:
			raise ValidationError('Descrição muito longa')
		return data

	def clean_enrollNum(self):
		data = self.cleaned_data['enrollNum']
		if len(data) < 12 and len(data) != 0:
			raise ValidationError('Número de matrícula muito curto')
		return data
