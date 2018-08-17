from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
)

from .models import MyUser


class AccountSer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'email',
            'name',
            'designation',
            'role',
            'is_active',
            'created_at',
            'last_login',
        ]
