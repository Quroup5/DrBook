from django.contrib import admin
from booking.models import DoctorInfo, VisitTime


@admin.register(DoctorInfo)
class DoctorInfoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'speciality', 'price', 'address')
    search_fields = (['date'])

@admin.register(VisitTime)
class VisitTimeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'patient', 'date', 'time')
    search_fields = (['date'])
