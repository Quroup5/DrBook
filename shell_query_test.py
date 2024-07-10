from datetime import datetime

from booking.models import DoctorInfo, VisitTime
from users.models import CustomUser, PatientInfo
from django.db.models import Q


u1 = CustomUser.objects.filter(id=6).first()
q1 = PatientInfo.objects.filter(patient=u1).first()
q1.balance = 10
spec = DoctorInfo.SPECIALITY_CHOICES[0][0]
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