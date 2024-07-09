from users.models import CustomUser, PatientInfo

u1 = CustomUser.objects.filter(id=6).first()
q1 = PatientInfo.objects.filter(patient=u1).first()
q1.balance = 10