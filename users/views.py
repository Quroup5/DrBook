# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect

from users.forms import SignUpForm, LoginForm
from django.views.generic import CreateView

from users.models import PatientInfo


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()  # This saves the user to the database
        info = PatientInfo(patient=user, balance=0.0)  # This line create a corresponding info object for that patient
        info.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')


@login_required
def display_profile(request):
    info = PatientInfo.objects.filter(patient=request.user).first()

    context = {
        'msg': '',
        'user': request.user,
        'info': info
    }
    return render(request, 'users/profile.html', context)


def home_display_view(request):
    return render(request, template_name="users/home.html")


@login_required
def increase_balance(request):
    return render(request, template_name="users/increase_balance.html")


@login_required
def payment(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        current_user = request.user
        info_object = PatientInfo.objects.filter(patient=current_user).first()
        initial = float(info_object.balance)
        info_object.balance = str(initial + amount)
        info_object.save()
        msg = f'Thanks. You paid {amount}, and your balance is now: {initial + amount}.'
        return render(request, template_name='booking/after_operation_message.html',
                      context={'msg': msg})

    return HttpResponse(content="Bad Request", status=400)
