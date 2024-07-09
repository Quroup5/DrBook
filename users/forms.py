from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import CustomUser


class LoginForm(AuthenticationForm):
    pass


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
#
#
# class SignUpFormPatient(UserCreationForm):
#     class Meta:
#         model = PatientInfo
#         fields = ['national_id', 'address']
