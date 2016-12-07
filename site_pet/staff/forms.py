from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=100)
    password = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput())

    def login(self, request):
        username = self.data.get('username')
        password = self.data.get('password')
        user = authenticate(username=username, password=password)
        return user
