from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.models import User, Group
from .forms import *
from django.contrib.auth.decorators import login_required
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
        roles.append({'role': role.name_plural, 'members': members})
    return render(request, 'members/index.html', {'roles': roles, 'name': 'members.index'})


@login_required
def add_member(request):
    if request.method == 'POST':
        form = NewMemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            role = form.cleaned_data['role']

            user = User.objects.create_user(username, email, password)
            try:
                import pdb; pdb.set_trace()
                if role.name == 'Tutor':
                    user.groups.add(Group.objects.get(name='tutors'))
                else:
                    user.groups.add(Group.objects.get(name='members'))
                member = Member()
                member.user = user
                member.name = name
                member.role = role
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
def add_tutor(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            
            user = User.objects.create_user(username, email, password)
            try:
                user.groups.add(Group.objects.get(name='tutors'))

                tutor = Member()
                tutor.name = name
                tutor.user = user
                tutor.role = MemberRole.objects.get(name='Tutor')
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
def all_tutors(request):
    tutors = []
    for user in Group.objects.get(name='tutors').user_set.all():
        member = Member.objects.filter(user=user)[0]
        tutors.append((member.id, member.name, member.user.username, member.pet.__str__()))
    return JsonResponse({'data': tutors}, safe=False)


@login_required
def all_members(request):
    json = {'data': [(x.id, x.name, x.user.get_username(
    ), x.user.email, x.role.name) for x in request.user.member.pet.members.all()]}
    return JsonResponse(json, safe=False)


@login_required
def edit_member(request):
    if Group.objects.get(name='admin') in request.user.groups.all():
        return HttpResponse('admin')
    member = request.user.member
    if request.method == 'POST':
        form = EditMemberForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            facebook_link = form.cleaned_data['facebook_link']
            lattes_link = form.cleaned_data['lattes_link']
            photo = form.cleaned_data['photo']

            user = User.objects.get(id=request.user.id)
            user.email = email
            photo.name = user.username

            member.name = name
            member.facebook_link = facebook_link
            member.lattes_link = lattes_link
            member.photo = photo

            user.save()
            member.save()
            return redirect(reverse('staff.index'))
        return render(request, 'members/edit_member.html', {'form': form}, status=400)
    form = EditMemberForm(initial={'name': member.name, 'email': member.user.email, 'old_email': member.user.email,
                                   'facebook_link': member.facebook_link, 'lattes_link': member.lattes_link, 'photo': member.photo})
    return render(request, 'members/edit_member.html', {'form': form})

@login_required
def edit_member_role(request):
    admin = Group.objects.get(name='admin')
    tutors = Group.objects.get(name='tutors')
    if admin in request.user.groups.all():
        return HttpResponse('admin')
    elif tutors in request.user.groups.all():
        return HttpResponse('tutor')
    return HttpResponse('not allowed')
