from django.shortcuts import render, redirect, reverse
from staff.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group


def auth_login(request):
    form = LoginForm(request.POST or None)
    context = {'form': form, 'name': 'staff.auth_login'}
    if request.POST and form.is_valid:
        user = form.login(request)
        if user:
            groups = [Group.objects.get(name='admin'), Group.objects.get(name='tutors'), Group.objects.get(name='members')]
            if not groups[0] in user.groups.all() and not groups[1] in user.groups.all() and not groups[2] in user.groups.all():
                return HttpResponse('Este usuário não é um administrador, tutor ou membro de algum PET e, portanto, não pode acessar o sistema.', status=403)
            login(request, user)
            if 'next' in request.GET and request.GET.get('next', ''):
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
        return render(request, 'staff/admin_index.html')
    if Group.objects.get(name='tutors') in user_groups:
        return render(request, 'staff/tutors_index.html')
    if Group.objects.get(name='members') in user_groups:   
        return render(request, 'staff/member_index.html')
    if request.user.is_authenticated():
        return HttpResponse('Este usuário não é um administrador, tutor ou membro de algum PET e, portanto, não pode acessar o sistema.', status=403)
    return redirect(reverse('staff.auth_login'))