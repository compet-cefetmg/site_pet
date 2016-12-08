from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    posts = []
    username = request.GET.get('pet', '')
    if username:
        user_query = get_list_or_404(User, username=username)
        posts = Post.objects.filter(user=user_query[0]).order_by('publish_date').all()
    else:
        posts = Post.objects.order_by('publish_date').all()
    users = User.objects.all()
    context = {'posts': posts, 'name': 'blog.index'}
    return render(request, 'blog/index.html', context)


def post(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post, 'name': 'blog.index'}
    return render(request, 'blog/post.html', context)


def all(request):
    posts = [(p.id, p.title, p.author.name, p.publish_date.strftime("%d/%m/%y")) for p in Post.objects.all()]
    json = {'data': posts}
    return JsonResponse(json, safe=False)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.user = request.user
            return HttpResponse('OK')
        context = {'name': 'blog.add_post', 'form': form}
        return render(request, 'blog/form.html', context, status=400)
    else:
        form = PostForm()
        context = {'name': 'blog.add_post', 'form': form}
        return render(request, 'blog/form.html', context)
