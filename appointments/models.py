from django.db import models
from patients.models import Patient
from accounts.models import MyUser
# Create your models here.


class Appointment(models):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE())
    logged_by = models.ForeignKey(MyUser, on_delete=models.CASCADE())
    description = models.TextField(max_length=300)
    assigned_to = models.ForeignKey(MyUser, on_delete=models.CASCADE())
    logged_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)


class AppointmentLog(models):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE())
    activity = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    activity_by = models.ForeignKey(MyUser, on_delete=models.CASCADE())


class Treatment(models):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE())
