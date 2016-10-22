from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User


def index(request):
    posts = []
    username = request.GET.get('pet', '')
    if username:
        user_query = get_list_or_404(User, username=username)
        posts = Post.objects.filter(user=user_query[0]).order_by('publish_date').all()
    else:
        posts = Post.objects.order_by('publish_date').all()
    users = User.objects.all()
    context = {'posts': posts, 'users': users, 'name': 'blog.index'}
    return render(request, 'blog/index.html', context)

def post(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post, 'name': 'blog.index'}
    return render(request, 'blog/post.html', context)
