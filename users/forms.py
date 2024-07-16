from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, Textarea

from .models import Comment


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'score']
        widgets = {'text': Textarea()}
