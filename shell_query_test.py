# This file is for testing queries in shell

from datetime import datetime

from booking.models import Doctor, VisitTime
from users.models import CustomUser, PatientInfo
from django.db.models import Q

u1 = CustomUser.objects.filter(id=6).first()
q1 = PatientInfo.objects.filter(patient=u1).first()
q1.balance = 10
spec = Doctor.SPECIALITY_CHOICES[0][0]
print(spec)
s = CustomUser.objects.filter(doctorinfo__speciality__exact=spec)
doctor_list = CustomUser.objects.select_related('doctorinfo'
                                                ).filter(doctorinfo__speciality__exact=spec).values(
    'id', 'first_name', 'last_name', 'doctorinfo__speciality', 'doctorinfo__address', 'doctorinfo__price'
)

time_list = VisitTime.objects.filter(
    Q(doctor__doctor__exact=s.first()) & Q(patient_id=None) & Q(date__gte=datetime.today()))
# time_list = VisitTime.objects.filter(Q(doctor__doctor__exact=doctor) & Q(patient_id=None) & Q(date__gte=today))
time_list = time_list.filter(Q(time__gt=datetime.now()))
selected_visit_time = VisitTime.objects.get(id=8)
price = selected_visit_time.doctor.price

# TODO: remove national id from patient info class
# TODO: add address and phone number to custom user class
# TODO: add comment class: each user can add comment to its past visit times
# TODO: in search page all should be able to see the comments of each doctor
# TODO: add a page for completing user info for phone number to use OTP
# TODO: in login add OTP if there is no number tell it should complete phone number
# TODO: complete search by name
# TODO: improve the front end style


