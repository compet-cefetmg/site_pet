from django.shortcuts import render, get_list_or_404, get_object_or_404
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
    users = User.objects.all()
    context = {'publications': publications, 'users': users, 'name': 'blog.index'}
    return render(request, 'blog/index.html', context)

def post(request, id):
    post = get_object_or_404(Publication, id=id)
    context = {'post': post, 'name': 'blog.index'}
    return render(request, 'blog/post.html', context)
