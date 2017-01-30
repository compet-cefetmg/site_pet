from django.shortcuts import render, redirect, reverse
from staff.forms import *
from members.models import Member
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.core.mail import send_mass_mail
from site_pet.settings import EMAIL_HOST_USER
from bs4 import BeautifulSoup


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


@user_passes_test(lambda user: user.member.role.name == 'admin')
def send_admin_message(request):
    if request.method == 'POST':
        form = AdminMessageForm(request.POST)
        if form.is_valid():
            pets = form.cleaned_data['pets']
            member_roles = form.cleaned_data['member_roles']
            members = Member.objects.filter(role__in=member_roles, pet__in=pets).all()
            # messages_list = [[form.cleaned_data['subject'], form.cleaned_data['message'],
            #              EMAIL_HOST_USER, [member.user.email]] for member in members]
            # send_mass_mail(tuple(messages_list), fail_silently=False)

            unreachable_members = []
            subject = form.cleaned_data['subject']
            html_message = form.cleaned_data['message']
            text_message = BeautifulSoup(html_message, 'html.parser').get_text()

            for member in members:
                try:
                    message = EmailMultiAlternatives(subject, text_message, EMAIL_HOST_USER, [member.user.email])
                    message.attach_alternative(html_message, 'text/html')
                    message.send(fail_silently=False)
                except:
                    unreachable_members.append(member)

            for member in unreachable_members:
                messages.error(request, member.name + ' (' + member.user.email + ') não recebeu o e-mail.')

            messages.success(request, str(len(members) - len(unreachable_members)) +
                             ' de ' + str(len(members)) + ' e-mails enviados com sucesso.')
            return render(request, 'staff/admin_message_form.html', {'form': AdminMessageForm()})
        return render(request, 'staff/admin_message_form.html', {'form': form}, status=400)
    return render(request, 'staff/admin_message_form.html', {'form': AdminMessageForm()})
