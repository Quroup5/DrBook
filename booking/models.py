from django.db import models

from users.models import CustomUser


class DoctorInfo(models.Model):
    # This is a field to model one to one relation with customusers of type doctor
    doctor = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    address = models.CharField(max_length=200, null=False)
    speciality = models.CharField(max_length=100, null=False)
    price = models.FloatField(null=False)
