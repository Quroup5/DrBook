from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm


# Create your views here.
class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class UserLoginView(CreateView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = UserLoginForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request, f"you are logged in as {username}")
                    return redirect('home')
                else:
                    messages.error(requset, "Error")
            else:
                messages.error(request, "Username or password incorrect")
        form = UserLoginForm()
        return render(request, 'login.html', {"form": form})


def home(requset):
    return render(requset, 'home.html')
