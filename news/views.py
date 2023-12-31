from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Post, Vote, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms



def post_list(request):
    posts = Post.objects.all()
    for post in posts:
        post.upvotes = post.votes.filter(value=1).count()
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    upvotes = post.votes.filter(value=Vote.UPVOTE).count()
    return render(request, 'post_detail.html', {'post': post, 'upvotes': upvotes})


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


class LoginView(auth_view.LoginView):
    template_name = 'login.html'
    next_page = 'post_list'


class LogoutView(auth_view.LogoutView):
    next_page = 'post_list'


@login_required
def upvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not Vote.objects.filter(user=request.user, post=post).exists():
        Vote.objects.create(value=Vote.UPVOTE, user=request.user, post=post)
    return redirect('post_detail', pk=post.pk)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    upvotes = post.votes.filter(value=Vote.UPVOTE).count()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'upvotes': upvotes, 'form': form})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.user == comment.author:
        comment.delete()
    return redirect('post_detail', pk=post_pk)


@login_required
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
    return render(request, 'post_edit.html', {'form': form, 'is_new': True})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=post.pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'is_new': False})


