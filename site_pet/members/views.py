from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404


def index(request, username=""):
    user_query = get_list_or_404(User, username=username)
    roles = []
    for role in MemberRole.objects.all():
        members = role.members.filter(user=user_query[0]).all()
        roles.append({'role': role.role, 'members': members})
    context = {'roles': roles }
    return render(request, 'members/index.html', context)
