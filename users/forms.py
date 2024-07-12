from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import CustomUser


class LoginForm(AuthenticationForm):
    pass


class UserLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
#
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#
#
# class UserRegisterForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = ['username', 'email', 'password1', 'password2']
#
#
# class UserLoginForm(AuthenticationForm):
#
#     class Meta:
#         fields = ['username', 'password']
