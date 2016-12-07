from django.shortcuts import render, redirect
from staff.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


def auth_login(request):
    form = LoginForm(request.POST or None)
    context = {'form': form, 'name': 'staff.login'}
    if request.POST and form.is_valid:
        user = form.login(request)
        if user:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('/')
        context['error'] = 'Usuário ou senha incorretos.'
        return render(request, 'staff/login.html', context)
    return render(request, 'staff/login.html', context)


def auth_logout(request):
    logout(request)
    return redirect('/')

def index(request):
    return render(request, 'staff/index.html', {'name': 'staff.index'})
