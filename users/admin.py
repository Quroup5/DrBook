from django.contrib import admin

from .models import User, Patient

admin.site.register(User)


@admin.register(Patient)
class PatientInfoAdmin(admin.ModelAdmin):
    list_display = (['__str__'])
