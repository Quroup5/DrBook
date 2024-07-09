from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import CustomUser


class LoginForm(AuthenticationForm):
    pass


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
