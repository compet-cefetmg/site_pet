from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404


def index(request, username=""):
    user = get_list_or_404(User, username=username)
    members = Member.objects.filter(user=user[0])
    context = {'members': members }
    return render(request, 'members/index.html', context)
