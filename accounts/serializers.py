from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
)

from .models import MyUser


class AccountSer(HyperlinkedModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'email',
            'name',
            'designation',
            'role',
            'is_active',
            'is_superuser',
            'is_staff',
            'created_at',
            'last_login',
            'password',
            'url',
        )
        read_only_fields = (
            'created_at',
            'last_login',
        )
        extra_kwargs = {'password': {'write_only': True}}



class PasswordSer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('password',)
        partial_update = True