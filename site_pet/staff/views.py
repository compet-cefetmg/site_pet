from django.shortcuts import render, redirect
from staff.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


def auth_login(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid:
        user = form.login(request)
        if user:
            login(request, user)
            if request.GET['next']:
                return redirect(request.GET['next'])
            else:
                return render(request)

    return render(request, 'staff/login.html', {'form': form, 'name': 'staff.login'})


def auth_logout(request):
    logout(request)
    return HttpResponse('OK!')

def index(request):
    return render(request, 'staff/index.html', {'name': 'staff.index'})
