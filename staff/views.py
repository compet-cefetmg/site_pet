from django.shortcuts import render, redirect, reverse
from staff.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def auth_login(request):
    form = LoginForm(request.POST or None)
    context = {'form': form, 'name': 'staff.auth_login'}
    if request.POST and form.is_valid():
        user = form.login(request)
        if user is None:
            context['error'] = 'Usuário ou senha incorretos.'
            return render(request, 'staff/login.html', context, status=401) 
        if not hasattr(user, 'member'):
            return HttpResponse('Este usuário não é um administrador, tutor ou membro de algum PET e, portanto, não pode acessar o sistema.', status=403)
        login(request, user)
        if 'next' in request.GET and request.GET.get('next', ''):
            return redirect(request.GET['next'], permanent=True)
        return redirect(reverse('staff.index'))
    return render(request, 'staff/login.html', context)


def auth_logout(request):
    logout(request)
    return redirect('/')

@login_required
def index(request):
    if request.user.member.role.name == 'admin':
        return render(request, 'staff/admin_index.html')
    if request.user.member.role.name == 'tutor':
        return render(request, 'staff/tutors_index.html')
    else:
        return render(request, 'staff/member_index.html')
    return redirect(reverse('staff.auth_login'))
