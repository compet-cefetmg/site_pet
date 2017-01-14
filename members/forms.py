from django import forms
from django.db import models
from django.forms import ModelForm
from .models import Member, MemberRole
from cefet.models import Pet
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User, Group


class MemberForm(forms.Form):
    name = forms.CharField(label='Nome', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    username = forms.CharField(
        label='Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

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


class NewMemberForm(MemberForm):
    role = forms.ModelChoiceField(label='Função', widget=forms.Select(attrs={
                             'class': 'form-control'}), queryset=MemberRole.objects.exclude(name='admin').all())


class TutorForm(MemberForm):
    pet = forms.ModelChoiceField(label='PET', widget=forms.Select(attrs={
                            'class': 'form-control'}), queryset=Pet.objects.all())


class EditTutorForm(forms.Form):
    pet = forms.ModelChoiceField(label='PET', widget=forms.Select(attrs={
                            'class': 'form-control'}), queryset=Pet.objects.all())
    is_active = forms.BooleanField(label='Tutor ativo', required=False)


class EditMemberForm(forms.Form):
    name = forms.CharField(label='Nome', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Foto', required=False)
    facebook_link = forms.CharField(label='Link do Facebook', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    lattes_link = forms.CharField(label='Link do Lattes', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    old_email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists() and self.data['old_email'] != data:
            raise ValidationError('E-mail já cadastrado.')
        return data    


class MemberRoleForm(forms.Form):
    role = forms.ModelChoiceField(label='Função', widget=forms.Select(attrs={'class': 'form-control'}), queryset=MemberRole.objects.exclude(name='admin').all())

