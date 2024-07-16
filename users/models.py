from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import time


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


class Doctor(models.Model):
    # This is a field to model one-to-one relation with Users of type doctor
    doctor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    SPECIALITY_CHOICES = (
        ("General", "General"),
        ("Cardiology", "Cardiology"),
        ("Dermatology", "Dermatology"),
        ("Emergency Medicine", "Emergency Medicine"),
        ("Endocrinology", "Endocrinology"),
        ("Gastroenterology", "Gastroenterology"),
        ("Neurology", "Neurology"),
        ("Oncology", "Oncology"),
        ("Pediatrics", "Pediatrics"),
        ("Psychiatry", "Psychiatry"),
    )
    speciality = models.CharField(max_length=200, choices=SPECIALITY_CHOICES)
    address = models.CharField(max_length=200, null=False)
    price = models.FloatField(null=False)

    def __str__(self):
        return f"Dr. {self.doctor.first_name} {self.doctor.last_name}"


class VisitTime(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=False)
    TIME_CHOICES = [
        (time(hour=15, minute=0), '3:00 PM'),
        (time(hour=15, minute=30), '3:30 PM'),
        (time(hour=16, minute=0), '4:00 PM'),
        (time(hour=16, minute=30), '4:30 PM'),
        (time(hour=17, minute=0), '5:00 PM'),
        (time(hour=17, minute=30), '5:30 PM'),
        (time(hour=18, minute=0), '6:00 PM'),
        (time(hour=18, minute=30), '6:30 PM'),
        (time(hour=19, minute=0), '7:00 PM'),
        (time(hour=19, minute=30), '7:30 PM'),
        (time(hour=20, minute=0), '8:00 PM'),
        (time(hour=20, minute=30), '8:30 PM'),
    ]
    time = models.TimeField(choices=TIME_CHOICES)

    class Meta:
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"Dr. {self.doctor.doctor.first_name} {self.doctor.doctor.last_name}"


class Comment(models.Model):
    visit_time = models.OneToOneField(VisitTime, on_delete=models.CASCADE, null=False)
    text = models.TextField(max_length=500, null=False)
    SCORES = (
        (0, 0),
        (0.5, 0.5),
        (1, 1),
        (1.5, 1.5),
        (2, 2),
        (2.5, 2.5),
        (3, 3),
        (3.5, 3.5),
        (4, 4),
        (4.5, 4.5),
        (5, 5),
    )
    score = models.FloatField(choices=SCORES)
