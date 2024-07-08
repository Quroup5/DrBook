# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.urls import reverse_lazy

from users.forms import SignUpForm
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    # success_url = reverse_lazy('login')
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It saves the form data to the database.
        user = form.save()  # This saves the user to the database
        # Additional logic can go here if needed
        return super().form_valid(form)


class UserLoginForm(AuthenticationForm):
    pass


def home_display_view(request):
    return render(request, template_name="users/home.html")
