from django.contrib import admin

# Register your models here.
from booking.models import DoctorInfo
from users.models import CustomUser

admin.site.register(CustomUser)
