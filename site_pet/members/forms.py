from django import forms
from django.db import models
from django.forms import ModelForm
from .models import Member, MemberRole
from cefet.models import Pet
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User, Group


class NewMemberForm(forms.Form):
    name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label='Papel', widget=forms.Select(attrs={'class': 'form-control'}), choices=[(x.id, x.name) for x in MemberRole.objects.all()])

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise ValidationError('Usuário já cadastrado.')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise ValidationError('E-mail já cadastrado.')
        return data


class EditMemberForm(forms.Form):
    name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    facebook_link = forms.CharField(label='Link do Facebook', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    lattes_link = forms.CharField(label='Link do Lattes', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    old_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists() and self.data['old_email'] != data:
            raise ValidationError('E-mail já cadastrado.')
        return data


class TutorForm(NewMemberForm):
    pet = forms.ChoiceField(label='PET', widget=forms.Select(attrs={'class': 'form-control'}), choices=[(p.id, p.__str__()) for p in Pet.objects.all()])

