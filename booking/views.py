from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from users.models import User, Doctor, VisitTime, Patient

import datetime


def home(request):
    # PageTree: 1
    return render(request, template_name="home.html")


def display_search_page(request):
    specs = [spec[0] for spec in Doctor.SPECIALITY_CHOICES]
    context = {
        'msg': '',
        'specs': specs
    }
    return render(request, template_name="booking/search.html", context=context)


def search_by_name(request):
    doctor_list = None

    if request.method == "GET":

        first_name = request.GET.get("first_name", '')
        last_name = request.GET.get("last_name", '')

        if len(first_name) == 0 and len(last_name) == 0:
            doctor_list = User.objects.select_related('doctor').filter(
                Q(doctor__user__first_name__startswith='')
                |
                Q(doctor__user__last_name__istartswith='')).values(
                'id', 'first_name', 'last_name', 'doctor__speciality', 'doctor__address', 'doctor__price'
            )

        if len(first_name) == 0 and len(last_name) != 0:
            doctor_list = User.objects.select_related('doctor').filter(
                Q(doctor__user__last_name__istartswith=last_name)).values(
                'id', 'first_name', 'last_name', 'doctor__speciality', 'doctor__address', 'doctor__price'
            )

        if len(first_name) != 0 and len(last_name) == 0:
            doctor_list = User.objects.select_related('doctor').filter(
                Q(doctor__user__first_name__istartswith=first_name)).values(
                'id', 'first_name', 'last_name', 'doctor__speciality', 'doctor__address', 'doctor__price'
            )

        if len(first_name) != 0 and len(last_name) != 0:
            doctor_list = User.objects.select_related('doctor').filter(
                Q(doctor__user__first_name__startswith=first_name)
                &
                Q(doctor__user__last_name__istartswith=last_name)).values(
                'id', 'first_name', 'last_name', 'doctor__speciality', 'doctor__address', 'doctor__price'
            )

        context = {
            'doctor_list': doctor_list
        }
        return render(request, template_name='booking/search_result.html', context=context)

    return HttpResponse(content="Bad Request", status=400)


def search_by_speciality(request):
    if request.method == "GET":
        spec = request.GET.get("spec")
        doctor_list = User.objects.select_related('doctor'
                                                  ).filter(doctor__speciality__exact=spec).values(
            'id', 'first_name', 'last_name', 'doctor__speciality', 'doctor__address', 'doctor__price'
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
        time_list = VisitTime.objects.filter(Q(doctor__user__exact=doctor) & Q(patient_id=None) & Q(date__gte=today))
        time_list = time_list.filter(Q(date__gte=datetime.datetime.now())).order_by('date', 'time')

        context = {
            'doctor': doctor,
            'time_list': time_list
        }
        return render(request, template_name='booking/visit_times.html', context=context)

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
def reserve_visit_times(request):
    if request.method == "POST":

        time_id = request.GET.get("id")

        selected_visit_time = VisitTime.objects.get(id=time_id)
        price = selected_visit_time.doctor.price
        info_object = Patient.objects.filter(user=request.user).first()

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
def show_reservations(request):
    time_list = VisitTime.objects.filter(patient__user__exact=request.user)
    context = {
        'msg': '',
        'times': time_list
    }

    return render(request, template_name="booking/show_reservations.html", context=context)


@login_required
def display_past_visit_times(request):
    time_list = VisitTime.objects.filter(
        Q(patient__user__exact=request.user) & Q(date__lt=datetime.datetime.today())).order_by('date', 'time')
    context = {
        'msg': '',
        'times': time_list
    }

    return render(request, template_name="booking/display_past_visit_times.html", context=context)
