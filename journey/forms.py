from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'image_url', 'visited_places', 'visited_date', 'favorite_place', 'address', 'city', 'postal_code', 'favorite_activity', 'description', 'publish')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class SignUpForm(forms.ModelForm):
    phone = forms.CharField(help_text='Required')
    address = forms.CharField(help_text='Required')
    city = forms.CharField(help_text='Required')
    zip = forms.CharField(help_text='Required')

    class Meta:
        model = Post
        fields = ('phone', 'address', 'city', 'zip')


class CreateUserAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, help_text='Required')
    last_name = forms.CharField(max_length=20, help_text='Required')
    email = forms.EmailField(max_length=60, help_text='Required')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
