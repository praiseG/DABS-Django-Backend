from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,)

from .models import Appointment, Treatment


class AppointmentSer(HyperlinkedModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'patient',
            'logged_by',
            'assigned_to',
            'logged_at',
            'description',
            'comment',
            'status',
            'updated_at',
            'url',
        )
        # depth = 1
        read_only_fields = (
            'logged_at',
            'updated_at',
        )


class AppointmentLogSer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'patient',
            'logged_by',
            'assigned_to',
            'description',
            'status',
        )


class TreatmentSer(ModelSerializer):
    class Meta:
        model = Treatment
        fields = (
            'appointment',
            'diagnosis',
            'prescription',
        )
        depth = 1