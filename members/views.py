from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


def index(request):
    roles = []
    pet_id = request.GET.get('pet', '')
    if pet_id:
        pet = get_object_or_404(Pet, id=pet_id)
    for role in MemberRole.objects.order_by('name').all():
        if pet_id:
            members = role.members.filter(pet=pet).order_by('name').all()
        else:
            members = role.members.order_by('name').all()
        roles.append({'role': role.verbose_name_plural, 'members': members})
    return render(request, 'members/index.html', {'roles': roles, 'name': 'members.index'})


@login_required
@user_passes_test(lambda user: user.member.role.name == 'tutor')
def add_member(request):
    if request.method == 'POST':
        form = NewMemberForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data[
                                            'email'], password=form.cleaned_data['password'])
            try:
                member = Member()
                member.user = user
                member.name = form.cleaned_data['name']
                member.role = form.cleaned_data['role']
                member.pet = request.user.member.pet

                user.save()
                member.save()
                messages.success(request, 'Membro adicionado com sucesso.')
            except:
                user.delete()
                messages.error(request, 'Não foi possível adicionar o membro.')

            return redirect(reverse('staff.index'))
        return render(request, 'members/add_member.html', {'form': form}, status=400)
    else:
        return render(request, 'members/add_member.html', {'form': NewMemberForm()})


@login_required
@user_passes_test(lambda user: user.member.role.name == 'admin')
def add_tutor(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data[
                                            'email'], password=form.cleaned_data['password'])
            try:
                tutor = Member()
                tutor.name = form.cleaned_data['name']
                tutor.user = user
                tutor.role = MemberRole.objects.get(name='tutor')
                tutor.pet = form.cleaned_data['pet']

                user.save()
                tutor.save()
                messages.success(request, 'Tutor adicionado com sucesso.')
            except:
                user.delete()
                messages.error(request, 'Não foi possível adicionar o tutor.')

            return redirect(reverse('staff.index'))
        return render(request, 'members/add_tutor.html', {'form': form}, status=400)
    else:
        form = TutorForm()
        return render(request, 'members/add_tutor.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.member.role.name == 'admin')
def all_tutors(request):
    tutors = [(member.id, member.name, member.user.username, member.pet.__str__())
              for member in MemberRole.objects.get(name='tutor').members.all()]
    return JsonResponse({'data': tutors}, safe=False)


@login_required
@user_passes_test(lambda user: user.member.role.name in ['admin', 'tutor'])
def all_members(request):
    members = [(member.id, member.name, member.user.username, member.user.email, member.role.verbose_name)
               for member in request.user.member.pet.members.all()]
    return JsonResponse({'data': members}, safe=False)


@login_required
def edit_personal_info(request):
    member = request.user.member
    if request.method == 'POST':
        form = EditMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member.user.email = form.cleaned_data['email']
            member.name = form.cleaned_data['name']

            if form.cleaned_data['facebook_link']:
                member.facebook_link = form.cleaned_data['facebook_link']
            if form.cleaned_data['lattes_link']:
                member.lattes_link = form.cleaned_data['lattes_link']
            if form.cleaned_data['photo']:
                photo.name = user.username
                member.photo = photo = form.cleaned_data['photo']

            member.user.save()
            member.save()
            messages.success(request, 'Informações atualizadas com sucesso.')
            return redirect(reverse('members.edit_personal_info'))

        messages.error(request, 'Não foi possível atualizar as informações.')
        return render(request, 'members/edit_personal_info.html', {'form': form}, status=400)

    form = EditMemberForm(initial={'name': member.name, 'email': member.user.email, 'old_email': member.user.email,
                                   'facebook_link': member.facebook_link, 'lattes_link': member.lattes_link, 'photo': member.photo})
    return render(request, 'members/edit_personal_info.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.member.role.name in ['admin', 'tutor'])
def edit_member(request, username):
    user = get_object_or_404(User, username=username)
    member = user.member

    if request.user.member.role.name == 'admin':
        return HttpResponse('admin')

    if request.user.member.role.name == 'tutor':
        if request.method == 'POST':
            form = MemberRoleForm(request.POST)

            if form.is_valid():
                member.role = form.cleaned_data['role']

                if form.cleaned_data['role'].name == 'ex-member':
                    user.is_active = False
                else:
                    user.is_active = True
                member.role = form.cleaned_data['role']

                member.save()
                user.save()
                messages.success(request, 'Informações atualizadas com sucesso.')
                return redirect(reverse('staff.index'))

        form = MemberRoleForm(initial={'role': member.role})
        return render(request, 'members/edit_member.html', {'form': form})

    return redirect(reverse('staff.auth_login', kwargs={'next': '/members/' + username + '/edit/'}))
