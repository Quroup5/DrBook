from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import CustomUser

class LoginForm(AuthenticationForm):
    pass

class SignUpForm(UserCreationForm):
    # username = forms.CharField(
    #     max_length=150,
    #     required=True,
    #     widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    # email = forms.EmailField(
    #     required=True,
    #     widget=forms.EmailInput(attrs={'class': 'form-control'})
    # )
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    #     label='password1',
    #     required=True
    # )
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    #     label='password2',
    #     required=True
    # )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
