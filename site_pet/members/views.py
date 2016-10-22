from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User


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
