from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedIdentityField

from .models import Patient

class PatientSer(HyperlinkedModelSerializer):
    # history = HyperlinkedIdentityField(
    #     view_name='patients:history',
    #     lookup_field='pk'
    # )

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
            # 'history',
            'url',

        )
        read_only_fields = ('registered_on', 'registered_by',)