from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from datetime import datetime

from django.views.generic import CreateView

from users.forms import SignUpForm, UserLoginForm
from django.contrib.auth.views import LoginView

from users.models import Patient, User
from users.otp import send_otp

import pyotp


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()  # This saves the user to the database
        info = Patient(patient=user, balance=0.0)  # This line create a corresponding info object for that patient
        info.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    # TODO: add Google login
    template_name = 'users/login.html'


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
                    user = get_object_or_404(User, username=username)
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    messages.success(request, f"you are logged in as {username}")
                    return redirect('home')

    return render(request, 'otp.html')


@login_required
def display_profile(request):
    info = Patient.objects.filter(patient=request.user).first()

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
        info_object = Patient.objects.filter(patient=current_user).first()
        initial = float(info_object.balance)
        info_object.balance = str(initial + amount)
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
    comments = Comment.objects.filter(visit_time__doctor__doctor_id=doctor_id)
    context = {
        'doctor': doctor,
        'comments': comments
    }
    print(comments.values())
    return render(request, template_name='booking/see_comments.html', context=context)
