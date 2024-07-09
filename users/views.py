# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy

from users.forms import SignUpForm, LoginForm
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    # success_url = reverse_lazy('login')
    success_url = reverse_lazy('login')

    def form_valid(self, form):

        user = form.save()  # This saves the user to the database

        return super().form_valid(form)



class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')

@login_required
def display_profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'users/profile.html', context)





def home_display_view(request):
    return render(request, template_name="users/home.html")
