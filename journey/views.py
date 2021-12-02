from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.db.models import Q

now = timezone.now()


def post_list(request):
    object_list = []
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '' or query is None:
            query = 'None'
            #Reference - https://stackoverflow.com/questions/44033670/python-django-rest-framework-unorderedobjectlistwarning
            object_list = Post.objects.all().order_by('-publish')
        else:
            object_list = Post.objects.order_by('-publish').filter(Q(title__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query) | Q(description__icontains=query))

    # object_list = Post.objects.all()

    paginator = Paginator(object_list, 6)  # 6 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'journey/post_list.html',
                  {'page': page,
                   'posts': posts})


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
            post.author = request.user
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
            if request.user.is_superuser:
                return redirect('journey:post_detail')
            else:
                request = HttpRequest()
                request.method = 'GET'
                return blog_post(request, post.pk)
    else:
        # edit
        form = PostForm(instance=post)
    return render(request, 'journey/post_edit.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    if request.user.is_superuser:
        return redirect('journey:post_detail')
    else:
        return redirect('journey:post_list')


def blog_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # List of active comments for this post
    comments = post.comments.filter()
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.name = request.user.first_name
            new_comment.email = request.user.email
            # Save the comment to the database
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'journey/blog_post.html',
                  {'post': post, 'comments': comments,
                   'comment_form': comment_form})


@login_required
def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'journey/comment_list.html',
              {'comments': comments})

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
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("journey:post_list")
    else:
        user_form = CreateUserAccountForm()
    return render(request, 'journey/signup.html', {'user_form': user_form})

