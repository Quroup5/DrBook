from django.contrib import admin

from .models import User, Patients

admin.site.register(User)


@admin.register(Patients)
class PatientInfoAdmin(admin.ModelAdmin):
    list_display = (['__str__'])
