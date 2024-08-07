from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from datetime import datetime

from django.views.generic import CreateView

import users.models
from users.forms import SignUpForm, UserLoginForm, PatientForm, DoctorForm, CommentForm
from django.contrib.auth.views import LoginView

from users.models import Patient, User, VisitTime, Comment
from users.otp import send_otp

import pyotp


class SignUpView(CreateView):
    object: users.models.User
    # PageTree: 2.2
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_form'] = PatientForm(self.request.POST or None)
        context['doctor_form'] = DoctorForm(self.request.POST or None)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)  # Set self.object to the user being created
        user = self.object
        user_type = form.cleaned_data['user_type']
        user.is_patient = user_type == 'patient'
        user.is_doctor = user_type == 'doctor'
        user.save()

        if user_type == 'patient':
            patient_form = PatientForm(self.request.POST)
            if patient_form.is_valid():
                patient = patient_form.save(commit=False)
                patient.user = user
                patient.save()
        elif user_type == 'doctor':
            doctor_form = DoctorForm(self.request.POST)
            if doctor_form.is_valid():
                doctor = doctor_form.save(commit=False)
                doctor.user = user
                doctor.save()

        login(self.request, user)
        return redirect(self.get_success_url())


class UserLoginView(LoginView):
    # TODO: add Google login
    # PageTree: 2.1
    template_name = 'users/login.html'
    authentication_form = UserLoginForm

    def get_success_url(self):
        return reverse('profile')


@login_required(login_url=reverse_lazy('login'))
def display_profile(request):
    info = Patient.objects.filter(user=request.user).first()

    context = {
        'msg': '',
        'user': request.user,
        'info': info
    }
    return render(request, 'users/profile.html', context)


@login_required
def increase_balance(request):
    return render(request, template_name="users/increase_balance.html")


@login_required
def payment(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        current_user = request.user
        info_object = Patient.objects.filter(user=current_user).first()
        initial = float(info_object.balance)
        info_object.balance = initial + amount
        info_object.save()
        msg = f'Thanks. You paid {amount}, and your balance is now: {initial + amount}.'
        return render(request, template_name='booking/after_operation_message.html',
                      context={'msg': msg})

    return HttpResponse(content="Bad Request", status=400)


@login_required
def add_comment(request):
    time_id = request.GET.get("time_id")
    selected_visit_time = VisitTime.objects.get(id=time_id)

    return render(request, template_name="booking/add_comment.html",
                  context={'form': CommentForm(), 'visit_time': selected_visit_time})


@login_required
def save_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        time_id = request.GET.get("time_id")
        selected_visit_time = VisitTime.objects.get(id=time_id)

        # This line help us find if there was a comment already
        old_comment = Comment.objects.filter(visit_time=selected_visit_time).first()

        if form.is_valid():
            text = form.cleaned_data['text']
            score = form.cleaned_data['score']

            if old_comment is None:
                comment = Comment(visit_time=selected_visit_time, text=text, score=score)
                comment.save()
                msg = 'Thanks. Your comment added!'

            else:
                old_comment.text = text
                old_comment.score = score
                old_comment.save()
                msg = 'Thanks. Your comment updated!'

            return render(request, template_name='booking/after_operation_message.html',
                          context={'msg': msg})

    return HttpResponse(content="Bad Request", status=400)


@login_required
def see_doctor_comments(request):
    doctor_id = request.GET.get("id")
    doctor = User.objects.get(id=doctor_id)
    comments = Comment.objects.filter(visit_time__doctor__user_id=doctor_id)
    context = {
        'doctor': doctor,
        'comments': comments
    }
    return render(request, template_name='booking/see_comments.html', context=context)


def otp(request):
    request = send_otp(request)
    if request.method == 'POST':
        otp_req = request.POST['otp']
        username = request.user.username

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_date = datetime.fromisoformat(otp_valid_date)

            if valid_date > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=1000)
                if totp.verify(otp_req, valid_window=10):
                    user = get_object_or_404(User, username=username)
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    messages.success(request, f"you are logged in as {username}")
                    return redirect('profile')
        else:
            messages.error(request, "OTP Error!")

    return render(request, 'otp.html')
