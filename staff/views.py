from django.shortcuts import render, redirect
from staff.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group


def auth_login(request):
    form = LoginForm(request.POST or None)
    context = {'form': form, 'name': 'staff.login'}
    if request.POST and form.is_valid:
        user = form.login(request)
        if user:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'], permanent=True)
            return redirect('/')
        context['error'] = 'Usuário ou senha incorretos.'
        return render(request, 'staff/login.html', context, status=401)
    return render(request, 'staff/login.html', context)


def auth_logout(request):
    logout(request)
    return redirect('/')


def index(request):
    user_groups = request.user.groups.all()
    if Group.objects.get(name='admin') in user_groups:
        return render(request, 'staff/admin_index.html', {'name': 'staff.index'})
    if Group.objects.get(name='tutors') in user_groups:
        return render(request, 'staff/tutors_index.html', {'name': 'staff.index'})
    return render(request, 'staff/member_index.html', {'name': 'staff.index'})




