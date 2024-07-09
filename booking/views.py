import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from booking.models import DoctorInfo, VisitTime
from users.models import CustomUser


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
        doctor_list = CustomUser.objects.select_related('doctorinfo'
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
        doctor = CustomUser.objects.get(id=doctor_id)
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


def reserve_visit_times(request):
    pass
