from django import forms
from django.db import models
from django.forms import ModelForm
from .models import Member, MemberRole
from cefet.models import Pet
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User, Group

class PersonalInfoForm(forms.Form):

    def __init__(self,*args,**kwargs):
        creating_user = kwargs.pop('required')
        super(PersonalInfoForm,self).__init__(*args,**kwargs)
        self.fields['name'].required=self.fields['email'].required=self.fields['start_date'].required=creating_user
        if not creating_user:
            self.fields['password_confirm'].widget=forms.HiddenInput()
            self.fields['password_confirm'].required=False

    old_email = forms.EmailField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label='Nome', widget=forms.TextInput(
        attrs={'class': 'form-control'}), help_text='Obrigatório para a finalização do cadastro *')
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Será necessário para fazer login e para receber notificações a respeito da homologação do cadastro *')
    photo = forms.ImageField(label='Foto', required=False)
    facebook_link = forms.CharField(label='Link do Facebook', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False, help_text='Copie e cole aqui o link inteiro')
    lattes_link = forms.CharField(label='Link do Lattes', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False, help_text='Copie e cole aqui o link inteiro')
    github_link = forms.CharField(label='Link do GitHub', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False, help_text='Copie e cole aqui o link inteiro')
    start_date = forms.DateField(label='Data de entrada no PET', widget=forms.DateInput(
        attrs={'class': 'datepicker'}, format=('%d/%m/%Y')), help_text='Obrigatório para a finalização do cadastro *')
    leave_date = forms.DateField(label='Data de saída do PET', widget=forms.DateInput(
        attrs={'class': 'datepicker', 'id':'leave_date'}, format=('%d/%m/%Y')), required=False, help_text='Deixe em branco se ainda fizer parte do PET. O preenchimento desse campo indica que você já terminou suas atividades no PET.')
    mensage = forms.CharField(label='Mensagem de ex-petiano',widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False) 
    password = forms.CharField(
        label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text='Obrigatório para a finalização do cadastro *')
    password_confirm = forms.CharField(
        label='Confirme sua senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text='Obrigatório para a finalização do cadastro *')

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            if self.fields['email'].required:
                if (User.objects.filter(email=data).exists()):
                    raise ValidationError('E-mail já cadastrado.')
                return data
            else:
                if data != self.cleaned_data['old_email'] and (User.objects.filter(email=data).exists() or Member.objects.filter(email=data).exists()):
                    raise ValidationError('E-mail já cadastrado.')
                return data
        except KeyError:
            raise ValidationError('Algo deu errado ao salvar seu e-mail. Por favor, tente novamente.')
        return data# Não permite registrar dois e-mails identicos no banco de dados

    def clean_leave_date(self):
        try:
            if self.cleaned_data['leave_date'] and not self.cleaned_data['start_date']:
                raise ValidationError('Você não pode definir uma data de saída sem definir uma data de entrada.')
            if self.cleaned_data['leave_date'] and self.cleaned_data['leave_date'] <= self.cleaned_data['start_date']:
                raise ValidationError('Sua data de saída não pode ser anterior a sua data de entrada.')
        except KeyError:
            raise ValidationError('Algo deu errado ao salvar as datas solicitadas. Por favor, tente novamente.')
        return self.cleaned_data['leave_date']# Não permite registrar data de saída sem a existência de uma data de entrada e não permite uma data de saída anterior a de entrada

    def clean_password_confirm (self):
        if self.fields['password_confirm'].required:
            data = self.cleaned_data['password']
            data2 = self.cleaned_data['password_confirm']
            if data != data2:
                raise ValidationError('Senha não confere com a anterior.')
        return self.cleaned_data['password_confirm']

    def clean_password (self):
        if not self.fields['password_confirm'].required:
            data = self.cleaned_data['password']
            if not User.objects.get(email=self.cleaned_data['old_email']).check_password(data):
                raise ValidationError('Senha inválida.')
        return self.cleaned_data['password']

class MemberRequest(PersonalInfoForm):
    #publish_as_team = forms.ChoiceField(label='Teste',widget=forms.RadioSelect(attrs={'class': 'radio'}), choices=[(True, 'Sim'), (False, 'Não')]) É um exemplo para quando precisar de um formulário contendo radioInput
    #teste = forms.BooleanField(label='Teste', widget=forms.CheckboxInput(attrs={'class': 'check'}), required=False)
    role = forms.ModelChoiceField(label='Função', widget=forms.Select(attrs={
        'class': 'form-control'}), queryset=MemberRole.objects.exclude(name='admin').all(), help_text='Obrigatório para a finalização do cadastro *')
    pet = forms.ModelChoiceField(label='PET', widget=forms.Select(attrs={
        'class': 'form-control'}), queryset=Pet.objects.all(), help_text='Obrigatório para a finalização do cadastro *')


    def clean_pet (self): # só permite cadastro de membros de PETs que já tenham Tutores (já queo tutor que deve aceitar ou recursar a solicitação)
        data = self.cleaned_data['pet']
        role = self.cleaned_data['role']
        if role.verbose_name != 'Tutor':
            try:
                tutor = Member.objects.filter(role=MemberRole.objects.get(verbose_name='Tutor'), autorized=True, pet=self.cleaned_data['pet'])
                if not tutor:
                    raise ValidationError('O(A) tutor(a) do PET de ' + str(data) + ' não tem cadastro confirmado neste site, isso impossibilita seu cadastro.')
            except KeyError:
                raise ValidationError('Algo deu errado ao salvar seu PET. Por favor, tente novamente.')
        return self.cleaned_data['pet']


class MemberRoleForm(forms.Form):
    role = forms.ModelChoiceField(label='Função', widget=forms.Select(
        attrs={'class': 'form-control'}), queryset=MemberRole.objects.exclude(name='admin').all())
