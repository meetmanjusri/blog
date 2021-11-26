from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'image_url', 'visited_places', 'visited_date', 'favorite_place', 'address', 'city', 'postal_code', 'favorite_activity', 'description', 'publish')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
