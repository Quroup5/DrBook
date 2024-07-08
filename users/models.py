from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


# Create your models here.



class CustomUser(AbstractUser):
    is_admin = models.BooleanField(null=True)
    #doctor_info = models.OneToOneField(DoctorInfo, on_delete=models.CASCADE, )

