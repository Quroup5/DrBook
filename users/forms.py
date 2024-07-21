from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment, User, Patient, Doctor


class UserLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password."
        ),
    }


class SignUpForm(UserCreationForm):
    CHOICES = [
        ('doctor', 'Sign Up as Doctor'),
        ('patient', 'Sign Up as Patient'),
    ]

    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    national_id = forms.CharField(max_length=10, required=True, help_text='Enter a valid 10-digit national ID.')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'national_id']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['speciality', 'address', 'price']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'score']
        widgets = {'text': forms.Textarea()}
