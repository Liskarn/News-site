from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'news/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'news/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'news/post_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def upvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Vote.objects.create(value=Vote.UPVOTE, user=request.user, post=post)
    return redirect('post_detail', pk=post.pk)

@login_required
def downvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Vote.objects.create(value=Vote.DOWNVOTE, user=request.user, post=post)
    return redirect('post_detail', pk=post.pk)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'news/post_edit.html', {'form': form})