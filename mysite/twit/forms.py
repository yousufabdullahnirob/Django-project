from django import forms
from .models import Tweet, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo',]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove max length validation on username field
        self.fields['username'].max_length = None
        self.fields['username'].widget.attrs.pop('maxlength', None)
        