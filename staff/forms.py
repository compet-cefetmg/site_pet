from django import forms
from django.contrib.auth import authenticate
from django_summernote.widgets import SummernoteWidget
from cefet.models import Pet
from members.models import MemberRole


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def login(self, request):
        username = self.data.get('username')
        password = self.data.get('password')
        user = authenticate(username=username, password=password)
        return user


class AdminMessageForm(forms.Form):
    member_roles = forms.ModelMultipleChoiceField(label='Mandar para os membros', queryset=MemberRole.objects.exclude(name='admin').all(
    ), widget=forms.SelectMultiple(attrs={'class': 'form-control'}), help_text='Somente os membros com as funções selecionadas receberão o e-mail.')
    pets = forms.ModelMultipleChoiceField(label='Dos seguintes grupos', queryset=Pet.objects.all(), widget=forms.SelectMultiple(
        attrs={'class': 'form-control'}), help_text='Somente os membros dos grupos PET selecionados receberão o e-mail.')
    subject = forms.CharField(label='Assunto', max_length=140, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Mensagem', widget=SummernoteWidget())
