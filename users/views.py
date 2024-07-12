# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from datetime import datetime
from users.forms import SignUpForm, LoginForm, UserLoginForm
from django.views.generic import CreateView
import pyotp
from users.models import PatientInfo, CustomUser
from users.otp import send_otp


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()  # This saves the user to the database
        info = PatientInfo(patient=user, balance=0.0)  # This line create a corresponding info object for that patient
        info.save()
        return super().form_valid(form)


# --------------------------


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
        return render(request, 'users/login.html', {"form": form})


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


def otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_date = datetime.fromisoformat(otp_valid_date)

            if valid_date > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(CustomUser, username=username)
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    messages.success(request, f"You are logged in as {username}")
                    return redirect('profile')
                else:
                    messages.error(request, f"Wrong OTP")

    return render(request, 'users/otp.html')
