from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    national_id = models.CharField(max_length=10,
                                   validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit national ID.')],
                                   null=True)


class Patients(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=255)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} {self.user.first_name} {self.user.last_name}"
