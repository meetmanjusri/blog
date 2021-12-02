from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateInput


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
        'title', 'image_url', 'visited_places', 'visited_date', 'favorite_place', 'address', 'city', 'postal_code',
        'favorite_activity', 'description')
        # Reference - https://stackoverflow.com/questions/41224035/django-form-field-label-how-to-change-its-value-if-it-belongs-to-a-certain-fi
        labels = {'visited_date': "Visited Date"}
        # Reference https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django
        widgets = {'visited_date': DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'})}

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['visited_places'].required = False
        self.fields['visited_date'].required = False
        self.fields['favorite_place'].required = False
        self.fields['address'].required = False
        self.fields['city'].required = False
        self.fields['postal_code'].required = False
        self.fields['favorite_activity'].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class CreateUserAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, help_text='Required')
    last_name = forms.CharField(max_length=20, help_text='Required')
    email = forms.EmailField(max_length=60, help_text='Required')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
