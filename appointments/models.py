from django.db import models
from patients.models import Patient
from accounts.models import MyUser
# Create your models here.


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    logged_by = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    description = models.TextField(max_length=300)
    assigned_to = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='doctor_assigned')
    logged_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)


class AppointmentLog(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT)
    activity = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    activity_by = models.ForeignKey(MyUser, on_delete=models.PROTECT)


class Treatment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT)
