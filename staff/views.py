from django.shortcuts import render, redirect, reverse
from staff.forms import LoginForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from members.models import Member, MemberRole
from members.models import Pet


def auth_login(request):
    form = LoginForm(request.POST or None)
    context = {'form': form}
    if request.POST and form.is_valid():
        user = form.login(request)
        if user is None:
            context['error'] = 'Usuário ou senha incorretos.'
            return render(request, 'staff/login.html', context, status=401)
        elif user.is_superuser:
            login(request, user)
            return redirect(reverse('staff.index'))
        elif not hasattr(user, 'member'):
            context['error']= 'Este usuário não é um administrador, tutor ou membro de algum PET e, portanto, não pode acessar o sistema.'
            return render(request, 'staff/login.html', context, status=403)
        elif not user.member.autorized:
            context['error'] = 'Este usuário ainda não foi homologado.'
            return render(request, 'staff/login.html', context, status=403)
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
    if request.user.is_superuser:
        pet_id = request.GET.get('pet', '')
        vetor=[]
        if pet_id:
            pet = get_object_or_404(Pet, id=pet_id)
            vetor1={
                'members': Member.objects.filter(autorized=False, pet=pet),
                'autorized': False,
                'title': 'PET de ' + str(pet) + ' integrantes não autorizados',
            }
            vetor2={
                'members': Member.objects.filter(autorized=True, pet=pet),
                'autorized': True,
                'title': 'PET de ' + str(pet) + ' integrantes autorizados',
            }
            vetor=[vetor1, vetor2]
        else:
            for pet in Pet.objects.all():
                vetor1={
                    'members': Member.objects.filter(autorized=False, pet=pet),
                    'autorized': False,
                    'title': 'PET de ' + str(pet) + ' integrantes não autorizados',
                }
                vetor2={
                    'members': Member.objects.filter(autorized=True, pet=pet),
                    'autorized': True,
                    'title': 'PET de ' + str(pet) + ' integrantes autorizados',
                }
                vetor+=[vetor1, vetor2]

        return render(request, 'staff/index.html', { 'name': 'staff.index', 'vetor': vetor, 'delete_url': 'staff.delete_member', 'paper': 'administrador', 'functions': 'remover e validar inscrições de qualquer pessoa'})
    elif request.user.member.role.name == 'Tutor':
        members = []
        for member in Member.objects.filter(autorized=False, pet=request.user.member.pet):
            if member.role.verbose_name!='Tutor':
                members.append(member)
        not_autorized = {
            'members': members,
            'autorized': False,
            'title': 'Membros não autorizados',
        }
        members = []
        for member in Member.objects.filter(autorized=True, pet=request.user.member.pet):
            if member.role.verbose_name!='Tutor':
                members.append(member)
        autorized = {
            'members': members,
            'autorized': True,
            'title': 'Membros autorizados',
        }

        return render(request, 'staff/index.html', {'vetor': [not_autorized, autorized], 'delete_url': 'staff.delete_member', 'paper': 'tutor', 'functions': 'remover e validar inscrições de membros do PET em que você faz parte'})
    else:
        return render(request, 'staff/index.html')
        #return render(request, 'staff/member_index.html')
    return redirect(reverse('staff.auth_login'))

@login_required
def autorize_member(request, id, autorize):
    member = get_object_or_404(Member, pk=id)
    if request.user.is_superuser | Member.objects.filter(user=request.user, role=MemberRole.objects.filter(verbose_name='Tutor')).exists():
        message = []
        subject = []
        if autorize:
            if member.leave_date:
                subject = 'Inscrição no site dos PETs do CEFET-MG autorizada'
                message = 'Parabéns!! Agora você está registrado como Ex-' + str(member.role) + ' no site: pet.cefetmg.br\n\nCaso queira alterar algum dado entre em contato grupo.compet@gmail.com'
            else:
                subject = 'Inscrição no site dos PETs do CEFET-MG confirmada'
                message = 'Parabéns!! Agora você já pode ter acesso interno ao site.\n\nUsuário: ' + str(member.user.username) + '\n\nAcesse o site: pet.cefetmg.br'
        else:
            subject = 'Inscrição bloqueada no site dos PETs do CEFET-MG'
            message = 'Sua inscrição no PET de ' + str(member.pet) + '!!\n\nPara mais informações entre em contato com ' + Member.objects.filter(user=request.user, role=MemberRole.objects.filter(verbose_name='Tutor')).email
        try:
            member.autorized = autorize
            print("Autorizou")
            print(member.name)
            print(member.autorized)
            member.save()
            #send_mail(subject, message, 'grupo.compet@gmail.com', [member.email])
        except:
            messages.error(request, 'Algo deu errado. Por favor, tente novamente.')
    return redirect(reverse('staff.index'))

@login_required
def delete_member(request, id):
    member = get_object_or_404(Member, pk=id)
    if request.user.is_superuser | Member.objects.filter(user=request.user, role=MemberRole.objects.filter(verbose_name='Tutor')).exists():
        email = member.email
        try:
            member.delete()
            member.user.delete()
            send_mail('Remoção da sua conta no site dos PETs do CEFET-MG', 'Sua conta não existe mais, caso não saiba o motivo, entre em contato com: ' + str(request.user.first_name) + ' em ' + str(request.user.email), 'grupo.compet@gmail.com', [member.email])
        except:
            messages.error(request, 'Algo deu errado. Por favor, tente novamente.')
    return redirect(reverse('staff.index'))
