from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from .models import *
from .forms import *
from django.shortcuts import render, redirect

now = timezone.now()


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'journey/post_list.html',
                  {'posts': posts})


@login_required
def post_detail(request):
    posts = Post.objects.all()
    return render(request, 'journey/post_detail.html',
                  {'posts': posts})


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
    comments = Comment.objects.all()
    return render(request, 'journey/comment_list.html',
                  {'comments': comments})


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


def signup(request):
    if request.method == 'POST':
        user_form = CreateUserAccountForm(request.POST)
        author_form = SignUpForm(request.POST)
        if author_form.is_valid() and user_form.is_valid():
            new_user = user_form.save()
            author = author_form.save(commit=False)
            author.user = new_user
            author.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("journey:post_list")
    else:
        user_form = CreateUserAccountForm()
        author_form = SignUpForm()
    return render(request, 'journey/signup.html', {'user_form': user_form, 'author_form': author_form})

