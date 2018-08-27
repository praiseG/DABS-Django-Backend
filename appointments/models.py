from django.db import models
from patients.models import Patient
from accounts.models import MyUser
# Create your models here.


class Appointment(models.Model):
    STATUSES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('queried', 'Queried'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    logged_by = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    description = models.TextField(max_length=400)
    comment = models.CharField(blank=True, null=True, max_length=255)
    assigned_to = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='doctor_assigned')
    logged_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUSES, default='new', max_length=15)

    def __str__(self):
        return self.assigned_to


class Treatment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT)
    diagnosis = models.TextField(max_length=400)
    prescription = models.TextField(max_length=400)

    def __str__(self):
        return self.appointment.patient.name
