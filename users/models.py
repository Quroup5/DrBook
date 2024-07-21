from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import time, timedelta, datetime


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    national_id = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                r'^\d{10}$',
                'Enter a valid 10-digit national ID.'
            )
        ],
        null=True
    )


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, verbose_name="Address")
    balance = models.PositiveIntegerField(default=0, verbose_name="Balance")

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    speciality = models.CharField(
        max_length=50,
        choices=SPECIALITY_CHOICES,
        verbose_name="Speciality",
        blank=True,
    )
    address = models.CharField(
        max_length=255,
        null=False,
        verbose_name="Address",
        blank=True,
    )
    price = models.FloatField(
        null=False,
        verbose_name="Consultation Fee",
        blank=True,
    )

    def __str__(self):
        return self.user.username


class VisitTime(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Doctor")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Patient")
    date = models.DateField(null=False, verbose_name="Date")

    @staticmethod
    def generate_time_choices(start_time, end_time, interval_minutes):
        times = []
        current_time = start_time
        while current_time < end_time:
            times.append((current_time, current_time.strftime('%I:%M %p')))
            current_time = (
                    datetime.combine(datetime.today(), current_time) + timedelta(minutes=interval_minutes)).time()
        return times

    TIME_CHOICES = generate_time_choices(time(15, 0), time(21, 0), 30)
    time = models.TimeField(choices=TIME_CHOICES, verbose_name="Time")

    class Meta:
        unique_together = ('doctor', 'date', 'time')
        verbose_name = "Visit Time"
        verbose_name_plural = "Visit Times"

    def __str__(self):
        return f"Dr. {self.doctor.user.get_full_name()}, Visit Time: {self.date} - {self.time.strftime('%I:%M %p')}"


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

    def __str__(self):
        return f"Comment by {self.visit_time.patient.user.username} about {self.visit_time}"
