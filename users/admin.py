from django.contrib import admin

# Register your models here.
from booking.models import DoctorInfo
from users.models import  User, Patients

admin.site.register(User)
#admin.site.register(PatientInfo)


@admin.register(Patients)
class PatientInfoAdmin(admin.ModelAdmin):
    list_display = (['__str__'])

