from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(null=True)


class PatientInfo(models.Model):
    patient = models.OneToOneField(CustomUser, on_delete=models.PROTECT, primary_key=True)
    national_id = models.CharField(max_length=10, unique=True, null=True,
                                   validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit national ID.')])
    address = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

