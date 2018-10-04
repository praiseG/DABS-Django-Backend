from rest_framework.serializers import (
    HyperlinkedModelSerializer, 
    HyperlinkedIdentityField,
    ModelSerializer
)

from .models import Patient

class PatientSer(ModelSerializer):
    # history = HyperlinkedIdentityField(
    #     view_name='patients:history',
    #     lookup_field='pk'
    # )

    class Meta:
        model = Patient
        fields = (
            'id',
            'name',
            'email',
            'mobile',
            'address',
            'age',
            # 'history',
            'disability',
            'registered_on',
            'registered_by',
        )
        read_only_fields = ('registered_on', 'registered_by', 'id')