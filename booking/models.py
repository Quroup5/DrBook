from django.db import models

# Create your models here.


class Transaction(models.Model):
    unique_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
