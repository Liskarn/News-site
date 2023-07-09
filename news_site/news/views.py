from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'post_detail.html', {'post': post})

@csrf_protect

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'post_form.html', {'form': form})

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
    return render(request, '/post_edit.html', {'form': form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
    return render(request, '/add_comment.html', {'form': form})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.user == comment.author:
        comment.delete()
    return redirect('post_detail', pk=post_pk)