from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import *
from .forms import *
from django.shortcuts import render, redirect

now = timezone.now()


def post_list(request):
    posts = Post.objects.all()
    print(posts)
    return render(request, 'journey/post_list.html',
                  {'post': posts})


@login_required
def post_detail(request):
    posts = Post.objects.filter(created_date__lte=timezone.now())
    return render(request, 'journey/post_detail.html',
                  {'post': posts})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = timezone.now()
            post.save()
            return redirect('journey:post_list')
    else:
        form = PostForm()
    return render(request, 'journey/post_new.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # update
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_date = timezone.now()
            post.save()
            return redirect('journey:post_list')
    else:
        # edit
        form = PostForm(instance=post)
    return render(request, 'journey/post_edit.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('journey:post_detail')


@login_required
def comment_list(request):
    comments = Comment.objects.filter(created_date__lte=timezone.now())
    return render(request, 'journey/comment_list.html',
                  {'comment': comments})


@login_required
def comment_new(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_date = timezone.now()
            comment.save()
            return redirect('journey:comment_list')
    else:
        form = CommentForm()
    return render(request, 'journey/comment_new.html', {'form': form})


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        # update
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.updated_date = timezone.now()
            comment.save()
            return redirect('journey:comment_list')
    else:
        # edit
        form = CommentForm(instance=comment)
    return render(request, 'journey/comment_edit.html', {'form': form})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('journey:comment_list')

