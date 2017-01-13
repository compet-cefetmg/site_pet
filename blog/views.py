from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse
from .models import Post
from .forms import PostForm
from cefet.models import Pet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages


def index(request):
    posts = []
    pet_id = request.GET.get('pet', '')
    if pet_id:
        pet = get_object_or_404(Pet, id=pet_id)
        posts = Post.objects.filter(
            member__in=pet.members.all()).order_by('publish_date').all()
    else:
        posts = Post.objects.order_by('publish_date').all()
    context = {'posts': posts, 'name': 'blog.index'}
    return render(request, 'blog/index.html', context)


def post(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post, 'name': 'blog.index'}
    return render(request, 'blog/post.html', context)


def all(request):
    posts = [(p.id, p.title, p.member.name, p.publish_date.strftime("%d/%m/%y"))
             for p in Post.objects.filter(member__in=request.user.member.pet.members.all()).all()]
    json = {'data': posts}
    return JsonResponse(json, safe=False)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.member = request.user.member
            post.save()
            return redirect(reverse('staff.index'))
        context = {'name': 'blog.add_post', 'form': form}
        return render(request, 'blog/form.html', context, status=400)
    else:
        form = PostForm()
        context = {'name': 'blog.add_post', 'form': form}
        return render(request, 'blog/form.html', context)


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.member.pet != request.user.member.pet:
        return HttpResponse('Unauthorized', status=400)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post editado com sucesso.')
            return redirect(reverse('staff.index'))
        return render(request, 'blog/form.html', {'form': form}, status=400)
    return render(request, 'blog/form.html', {'form': PostForm(instance=post)})


@login_required
def delete_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    if post.member.pet != request.user.member.pet or request.method != 'POST':
        return HttpResponse('Unauthorized', status=400)
    post.delete()
    return HttpResponse('OK', status=200)
