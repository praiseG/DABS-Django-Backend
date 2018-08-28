from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Patient


class PatientSer(HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = (
            'name',
            'email',
            'mobile',
            'address',
            'age',
            'disability',
            'registered_on',
            'registered_by',
            'url',
        )
        read_only_fields = ('registered_on', 'registered_by',)