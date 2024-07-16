import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from booking.forms import CommentForm
from booking.models import DoctorInfo, VisitTime, Comment
from users.models import User, Patients


def display_search_page(request):
    specs = [spec[0] for spec in DoctorInfo.SPECIALITY_CHOICES]
    context = {
        'specs': specs
    }
    return render(request, template_name="booking/search.html", context=context)


def search_by_name(request):
    pass


def search_by_speciality(request):
    if request.method == "GET":
        spec = request.GET.get("spec")
        doctor_list = User.objects.select_related('doctorinfo'
                                                  ).filter(doctorinfo__speciality__exact=spec).values(
            'id', 'first_name', 'last_name', 'doctorinfo__speciality', 'doctorinfo__address', 'doctorinfo__price'
        )

        context = {
            'doctor_list': doctor_list
        }
        return render(request, template_name='booking/search_result.html', context=context)

    return HttpResponse(content="Bad Request", status=400)


def show_visit_times(request):
    if request.method == "GET":
        doctor_id = request.GET.get("id")
        doctor = User.objects.get(id=doctor_id)
        today = datetime.date.today()
        # This query shows all the available visit time of after now
        time_list = VisitTime.objects.filter(Q(doctor__doctor__exact=doctor) & Q(patient_id=None) & Q(date__gte=today))
        time_list = time_list.filter(Q(time__gt=datetime.datetime.now())).order_by('date', 'time')
        context = {
            'doctor': doctor,
            'time_list': time_list
        }
        return render(request, template_name='booking/visit_times.html', context=context)

    return HttpResponse(content="Bad Request", status=400)


@login_required
def reserve_visit_times(request):
    if request.method == "POST":

        time_id = request.GET.get("id")

        selected_visit_time = VisitTime.objects.get(id=time_id)
        price = selected_visit_time.doctor.price
        info_object = Patients.objects.filter(user=request.user).first()

        balance = float(info_object.balance)
        msg = ''
        if balance - price < 0:
            msg = "Insufficient fund! Please increase your balance. "

        else:
            info_object.balance = str(balance - price)
            selected_visit_time.patient = info_object
            selected_visit_time.save()
            info_object.save()
            msg = "Successfully reserved!"

        context = {'msg': msg}
        return render(request,
                      template_name="booking/reservation_result_msg.html", context=context)

    return HttpResponse(content="Bad Request", status=400)


@login_required
def check_visit_times(request):
    if request.method == "GET":
        time_id = request.GET.get("id")
        selected_visit_time = VisitTime.objects.get(id=time_id)
        context = {
            'selected_time': selected_visit_time
        }
        return render(request, template_name='booking/check_visit_time.html', context=context)

    return HttpResponse(content="Bad Request", status=400)


@login_required
def show_reservations(request):

    time_list = VisitTime.objects.filter(patient__user_id=request.user.id)
    context = {
        'msg': '',
        'times': time_list
    }
    return render(request, template_name="booking/show_reservations.html", context=context)


@login_required
def reserve_visit_times(request):
    if request.method == "POST":

        time_id = request.GET.get("id")

        selected_visit_time = VisitTime.objects.get(id=time_id)
        price = selected_visit_time.doctor.price
        info_object = Patients.objects.filter(user=request.user).first()

        balance = float(info_object.balance)
        msg = ''
        if balance - price < 0:
            msg = "Insufficient fund! Please increase your balance. "

        else:
            info_object.balance = balance - price
            selected_visit_time.patient = info_object
            selected_visit_time.save()
            info_object.save()
            msg = "Successfully reserved!"

        context = {'msg': msg}
        return render(request,
                      template_name="booking/reservation_result_msg.html", context=context)

    return HttpResponse(content="Bad Request", status=400)


@login_required
def display_past_visit_times(request):
    time_list = VisitTime.objects.filter(
        Q(patient__user_id=request.user.id) & Q(date__lt=datetime.datetime.today())).order_by('date', 'time')
    context = {
        'msg': '',
        'times': time_list
    }

    return render(request, template_name="booking/display_past_visit_times.html", context=context)


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
