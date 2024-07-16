from datetime import datetime

from booking.models import DoctorInfo, VisitTime
from users.models import User, Patients
from django.db.models import Q

u1 = User.objects.filter(id=6).first()
q1 = Patients.objects.filter(patient=u1).first()
q1.balance = 10
spec = DoctorInfo.SPECIALITY_CHOICES[0][0]
print(spec)
s = User.objects.filter(doctorinfo__speciality__exact=spec)
doctor_list = User.objects.select_related('doctorinfo'
                                                ).filter(doctorinfo__speciality__exact=spec).values(
    'id', 'first_name', 'last_name', 'doctorinfo__speciality', 'doctorinfo__address', 'doctorinfo__price'
)

time_list = VisitTime.objects.filter(
    Q(doctor__doctor__exact=s.first()) & Q(patient_id=None) & Q(date__gte=datetime.today()))
# time_list = VisitTime.objects.filter(Q(doctor__doctor__exact=doctor) & Q(patient_id=None) & Q(date__gte=today))
time_list = time_list.filter(Q(time__gt=datetime.now()))

doctor_list = DoctorInfo.objects.filter(Q(doctor__first_name__startswith="amir")
                                                | Q(doctor__last_name__istartswith="amir")).values(
            'id', 'first_name', 'last_name', 'doctorinfo__speciality', 'doctorinfo__address', 'doctorinfo__price'
        )
doctor_list = User.objects.select_related('doctorinfo'
                                                  ).filter(Q(doctorinfo__doctor__first_name__startswith="ali")
                                                | Q(doctorinfo__doctor__last_name__istartswith="ali")).values(
            'id', 'first_name', 'last_name', 'doctorinfo__speciality', 'doctorinfo__address', 'doctorinfo__price'
        )