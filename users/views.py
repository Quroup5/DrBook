from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from .forms import UserRegisterForm


# Create your views here.
class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'

    def get(self, requset, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})
