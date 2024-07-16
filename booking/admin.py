from django.contrib import admin
from users.models import Doctor, VisitTime


@admin.register(Doctor)
class DoctorInfoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'speciality', 'price', 'address')
    search_fields = (['date'])


@admin.register(VisitTime)
class VisitTimeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'patient', 'date', 'time')
    search_fields = (['date'])
