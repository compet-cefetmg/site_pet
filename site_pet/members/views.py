from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404


def index(request, username=""):
    roles = []
    if username:
        user_query = get_list_or_404(User, username=username)
    for role in MemberRole.objects.order_by('name').all():
        if username:
            members = role.members.filter(user=user_query[0]).order_by('name').all()
        else:
            members = role.members.order_by('name').all()
        roles.append({'role': role.name_plural, 'members': members})
    context = {'roles': roles }
    return render(request, 'members/index.html', context)
