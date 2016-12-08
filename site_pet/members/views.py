from django.shortcuts import render, get_list_or_404, redirect, reverse
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from .forms import NewMemberForm, EditMemberForm
from django.contrib.auth.decorators import login_required


def index(request):
    roles = []
    username = request.GET.get('pet', '')
    if username:
        user_query = get_list_or_404(User, username=username)
    for role in MemberRole.objects.order_by('name').all():
        if username:
            members = role.members.filter(user=user_query[0]).order_by('name').all()
        else:
            members = role.members.order_by('name').all()
        roles.append({'role': role.name_plural, 'members': members})
    context = {'roles': roles, 'name' : 'members.index'}
    return render(request, 'members/index.html', context)


@login_required
def add_member(request):
    if request.method == 'POST':
        form = NewMemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            user = User.objects.create_user(username, email, password)
            return redirect(reverse('staff.index'))
        context = {'name': 'members.add_member', 'form': form}
        return render(request, 'members/form.html', context, status=400)
    else:
        form = NewMemberForm()
        context = {'name': 'members.add_member', 'form': form}
        return render(request, 'members/form.html', context)
