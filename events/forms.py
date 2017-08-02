# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.db import models
from django.forms import ModelForm, Form
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Event, Spectator

class EventForm(forms.Form):

	name = forms.CharField(label='Nome do evento', widget=forms.TextInput(attrs={'class': 'form-control'}))

	description = forms.CharField(label='Descrição', widget=forms.TextInput(attrs={'class': 'form-control'}))

	address = forms.CharField(label='Local', widget=forms.TextInput(attrs={'class': 'form-control'}))

	date = forms.DateField(label='Data', widget=forms.SelectDateWidget)

	beginTime = forms.TimeField(label='Horário de início')

	endTime = forms.TimeField(label='Horário de término')
