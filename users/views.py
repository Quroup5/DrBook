from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm
from .otp import send_otp
from datetime import datetime
import pyotp
from .models import User

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from users.models import Patients


# Create your views here.
class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()  # This saves the user to the database
        info = Patients(user=user, balance=0.0)  # This line create a corresponding info object for that patient
        info.save()
        return super().form_valid(form)


class UserLoginView(CreateView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

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
                    send_otp(request)
                    request.session['username'] = username
                    # login(request, user)
                    # messages.success(request, f"you are logged in as {username}")
                    return redirect('otp')
                else:
                    messages.error(request, "Error")
            else:
                messages.error(request, "Username or password incorrect")
        form = UserLoginForm()
        return render(request, 'users\login.html', {"form": form})


def home(request):
    return render(request, 'users\home.html')


def otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        username = request.session.get('username')

        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')

        if otp_secret_key and otp_valid_date is not None:
            valid_date = datetime.fromisoformat(otp_valid_date)

            if valid_date > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)

                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)

                    if 'otp_secret_key' in request.session:
                        del request.session['otp_secret_key']
                    if 'otp_valid_date' in request.session:
                        del request.session['otp_valid_date']

                    messages.success(request, f"you are logged in as {username}")
                    return redirect('profile')
                else:
                    messages.error(request, f"Wrong OTP")

    return render(request, 'users/otp.html')


@login_required
def display_profile(request):
    info = Patients.objects.filter(user=request.user).first()

    context = {
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
        info_object = Patients.objects.filter(user=current_user).first()
        initial = float(info_object.balance)
        info_object.balance = initial + amount
        info_object.save()
        url = reverse_lazy('profile')
        return HttpResponseRedirect(url)

    return HttpResponse(content="Bad Request", status=400)
