from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from .models import Publication
from django.contrib.auth.models import User


def index(request):
    publications = []
    username = request.GET.get('pet', '')
    if username:
        user_query = get_list_or_404(User, username=username)
        publications = Publication.objects.filter(user=user_query[0]).order_by('publish_date').all()
    else:
        publications = Publication.objects.order_by('publish_date').all()
    context = {'publications': publications }
    return render(request, 'blog/index.html', context)

def show(request, id):
    return HttpResponse(id)
