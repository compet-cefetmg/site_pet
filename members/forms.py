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


class PersonalInfoForm(forms.Form):
    name = forms.CharField(label='Nome', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Foto', required=False)
    facebook_link = forms.CharField(label='Link do Facebook', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    lattes_link = forms.CharField(label='Link do Lattes', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    start_date = forms.DateField(label='Data de entrada no PET', widget=forms.DateInput(
        attrs={'class': 'form-control', 'data-inputmask': '99/99/9999'}), required=False)
    leave_date = forms.DateField(label='Data de saída do PET', widget=forms.DateInput(
        attrs={'class': 'form-control'}), required=False, help_text='Deixa em branco se ainda fizer parte do PET.')
    old_email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            if User.objects.filter(email=data).exists() and self.data['old_email'] != data:
                raise ValidationError('E-mail já cadastrado.')
        except KeyError:
            raise ValidationError('Algo deu errado ao salvar seu e-mail. Por favor, tente novamente.')
        return data

    def clean_leave_date(self):
        if self.cleaned_data['leave_date'] and not self.cleaned_data['start_date']:
            raise ValidationError('Você não pode definir uma data de saída sem definir uma data de entrada.')
        if self.cleaned_data['leave_date'] and self.cleaned_data['leave_date'] <= self.cleaned_data['start_date']:
            raise ValidationError('Sua data de saída não pode ser anterior a sua data de entrada.')
        return self.cleaned_data['leave_date']


class MemberRoleForm(forms.Form):
    role = forms.ModelChoiceField(label='Função', widget=forms.Select(
        attrs={'class': 'form-control'}), queryset=MemberRole.objects.exclude(name='admin').all())
