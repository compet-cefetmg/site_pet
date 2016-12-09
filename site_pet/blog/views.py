from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse
from .models import Post
from .forms import PostForm
from cefet.models import Pet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    posts = []
    pet_id = request.GET.get('pet', '')
    if pet_id:
        pet = get_object_or_404(Pet, id=pet_id)
        users = [member.user for member in pet.members.all()]
        posts = Post.objects.filter(
            user__in=users).order_by('publish_date').all()
    else:
        posts = Post.objects.order_by('publish_date').all()
    context = {'posts': posts, 'name': 'blog.index'}
    return render(request, 'blog/index.html', context)


def post(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post, 'name': 'blog.index'}
    return render(request, 'blog/post.html', context)


def all(request):
    posts = [(p.id, p.title, p.author, p.publish_date.strftime("%d/%m/%y"))
             for p in Post.objects.all()]
    json = {'data': posts}
    return JsonResponse(json, safe=False)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form
            post.member = request.user.member
            post.save()
            return redirect(reverse('staff.index'))
        context = {'name': 'blog.add_post', 'form': form}
        return render(request, 'blog/form.html', context, status=400)
    else:
        form = PostForm()
        context = {'name': 'blog.add_post', 'form': form}
        return render(request, 'blog/form.html', context)
