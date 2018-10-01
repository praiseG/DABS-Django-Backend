from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
)

from .models import MyUser


class AccountSer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'id',
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
        )
        read_only_fields = (
            'created_at',
            'last_login',
            'id',
        )
        extra_kwargs = {'password': {'write_only': True}}


class UpdateSer(ModelSerializer):
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
        )


class PasswordSer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('password',)
        partial_update = True