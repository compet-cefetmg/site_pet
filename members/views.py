from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail

def index(request):
    roles = []
    current_members = []
    ex_members = []
    pet_id = request.GET.get('pet', '')
    if pet_id:
        pet = get_object_or_404(Pet, id=pet_id)
    for role in MemberRole.objects.exclude(name='admin').order_by('name').all():
        if pet_id:
            members = role.members.filter(pet=pet, autorized=True).order_by('name').all()
        else:
            members = role.members.filter(autorized=True).order_by('name').all()
        roles.append({'role': role.verbose_name_plural, 'members': members})

    #coloca todos os membros em um vetor
    for role in MemberRole.objects.exclude(name='admin').order_by('name').all():
        if pet_id:
            aux = role.members.filter(pet=pet, autorized=True).order_by('name').all()
        else:
            aux = role.members.filter(autorized=True).order_by('name').all()
        for member in aux:
            if not member.leave_date:
                current_members.append(member)
            else:
                ex_members.append(member)

    return render(request, 'members/index.html', {'roles': roles, 'name': 'members.index','current_members':current_members, 'ex_members':ex_members})

def add_member(request):
    context = {
        'title': "Inscrição",
        'text': "Preencha esse formulário para obter um login e ter acesso interno ao site"
    }

    if request.method == 'POST':
        form = MemberRequest(request.POST, request.FILES, required=True)

        if form.is_valid():
            #user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data[
            #                                'email'], password=form.cleaned_data['password'])
            try:
                member = Member()
                member.name = form.cleaned_data['name']
                member.email = member.old_email = form.cleaned_data['email']
                member.role = form.cleaned_data['role']
                member.pet = form.cleaned_data['pet']
                member.start_date = form.cleaned_data['start_date']
                if form.cleaned_data['facebook_link']:
                    member.facebook_link = form.cleaned_data['facebook_link']
                if form.cleaned_data['lattes_link']:
                    member.lattes_link = form.cleaned_data['lattes_link']
                if form.cleaned_data['github_link']:
                    member.github_link = form.cleaned_data['github_link']
                if form.cleaned_data['photo']:
                    member.photo = form.cleaned_data['photo']
                if form.cleaned_data['leave_date']:
                    member.leave_date = form.cleaned_data['leave_date']
                else:
                    
                    if(member.role == MemberRole.objects.get(verbose_name='Tutor')): # Tutor deve existir no banco de dados
                        #send_mail('Nova inscrição para Tutor do grupo PET de ' + str(member.pet), 'Nome: ' + str(member.name) + '\nE-mail: ' + str(member.email) + '\n\nAcesse o site: pet.cefetmg.br para avaliar a solicitação', 'grupo.compet@gmail.com', ['grupo.compet@gmail.com'])# manda e-mail para COMPET, e coloca na página do admin a opção de aceitar ou não o pedido
                        member.user = User.objects.create_user(member.email, member.email, form.cleaned_data['password'])
                        print("rola1")
                        member.user.name = member.name
                        print("rola1")
                        
                        member.user.save()
                        print("rola1")
                        
                        member.save()
                        print("rola1")
                        
                        messages.success(request, 'Tutor adicionado. Aguarde pela permissão do administrador poder acessar o site utilizando seu login. Você receberá um e-mail no endereço: ' + 
                        form.cleaned_data['email'] + ' quando for aceito.')
                    else:
                        tutor = Member.objects.filter(role=MemberRole.objects.get(verbose_name='Tutor'), pet=member.pet, autorized=True).first()
                        #send_mail('Nova inscrição para ' + str(member.role) +' do grupo PET de ' + str(member.pet), 'Nome: ' + str(member.name) + '\nE-mail: ' + str(member.email) + '\n\nAcesse o site: pet.cefetmg.br para avaliar a solicitação', 'grupo.compet@gmail.com', [tutor.email])# manda e-mail para COMPET, e coloca na página do admin a opção de aceitar ou não o pedido
                        member.user = User.objects.create_user(member.email, member.email, form.cleaned_data['password'])
                        member.user.name = member.name
                        member.user.save()  
                        member.save()
                        messages.success(request, str(member.role.verbose_name) + ' adicionado. Aguarde pela aceitação do tutor do PET ' + str(member.pet) + ' para poder acessar o site utilizando seu login. Você receberá um e-mail no endereço: ' + form.cleaned_data['email'] + ' quando for aceito.')
                        
                    return redirect(reverse('blog.index'))
            except:
                if member.id != None:
                    member.delete()
            messages.error(request, 'Algo deu errado no seu registro. Por favor, tente novamente.')
        else:
            messages.error(request, 'Algo deu errado no seu registro. Formulário inválido.')
    else:
        form = MemberRequest(required=True)
    context['form'] = form

    return render(request, 'blog/form.html', context)

@login_required
def edit_personal_info(request):
    context = {
        'title': "Atualização de dados",
        'text': "Atualize os seus dados utilizando essa página."
    }
    try:
        if request.method == 'GET':
            member = request.user.member
    except:
        context['form'] = PersonalInfoForm(required=False)
        return render(request, 'blog/form.html', context)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, required=False)
        if form.is_valid():
            try:
                member = request.user.member
                if form.cleaned_data['email']:
                    member.user.old_email = member.user.email = member.email = member.user.username = form.cleaned_data['email']
                if form.cleaned_data['name']:
                    member.name = form.cleaned_data['name']
                if form.cleaned_data['facebook_link']:
                    member.facebook_link = form.cleaned_data['facebook_link']
                if form.cleaned_data['lattes_link']:
                    member.lattes_link = form.cleaned_data['lattes_link']
                if form.cleaned_data['github_link']:
                    member.github_link = form.cleaned_data['github_link']
                if form.cleaned_data['start_date']:
                    member.start_date = form.cleaned_data['start_date']
                if form.cleaned_data['photo']:
                    member.photo.name = member.user.username
                    member.photo = form.cleaned_data['photo']
                member.user.save()

                if form.cleaned_data['leave_date']:
                    member.leave_date = form.cleaned_data['leave_date']
                    member.save()
                    member.user.delete()
                    messages.success(request, 'Informações atualizadas com sucesso. Agradecemos pelo período de colaboração com o PET de ' + str(member.pet))
                    return redirect(reverse('blog.index'))
                member.save()
                messages.success(request, 'Informações atualizadas com sucesso.')
            except:
                messages.error(request, 'Não foi possível atualizar suas informações. Algo deu errado.')

            return redirect(reverse('members.edit_personal_info'))
        else:
            messages.error(request, 'Não foi possível atualizar suas informações. Formulário não válido')
            context['form'] = form
            return render(request, 'blog/form.html', context, status=400)

    form = PersonalInfoForm(required=False, initial={'name': member.name, 'email': member.email, 'facebook_link': member.facebook_link,
    'lattes_link': member.lattes_link,'github_link': member.github_link, 'start_date': member.start_date, 'leave_date': member.leave_date, 'photo': member.photo, 'old_email': member.email})

    context['form'] = form
    return render(request, 'blog/form.html', context)
