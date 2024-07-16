from django.contrib import admin

# Register your models here.
from booking.models import Doctor
from users.models import CustomUser, PatientInfo

admin.site.register(CustomUser)
#admin.site.register(PatientInfo)


@admin.register(PatientInfo)
class PatientInfoAdmin(admin.ModelAdmin):
    list_display = (['__str__'])

