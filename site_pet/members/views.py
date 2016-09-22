from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    context = {'members': Member.objects.all()}
    return render(request, 'members/index.html', context)
