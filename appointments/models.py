from django.db import models
from safedelete.models import (
    SafeDeleteModel,
    NO_DELETE
)
from patients.models import Patient
from accounts.models import MyUser
# Create your models here.


class Appointment(SafeDeleteModel):
    _safedelete_policy = NO_DELETE

    STATUSES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('queried', 'Queried'),
    )
    patient = models.ForeignKey(Patient)
    logged_by = models.ForeignKey(MyUser)
    description = models.TextField(max_length=400)
    date = models.DateTimeField()
    comment = models.CharField(blank=True, null=True, max_length=255)
    assigned_to = models.ForeignKey(MyUser, related_name='doctor_assigned')
    logged_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUSES, default='new', max_length=15)

    def __str__(self):
        return "for {} by Dr {}".format(self.patient, self.assigned_to)


class Treatment(SafeDeleteModel):
    _safedelete_policy = NO_DELETE
    appointment = models.ForeignKey(Appointment)
    diagnosis = models.TextField(max_length=400)
    prescription = models.TextField(max_length=400)

    def __str__(self):
        return "for {}".format(self.appointment.patient.name)
