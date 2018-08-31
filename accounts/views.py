from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
   IsAdminUser
)

from .permissions import (
    IsAdminOrStaff, IsAdminOrIsSelf
)

from rest_framework.response import Response
from rest_framework.status import (
   HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
)
from rest_framework.decorators import action
from .serializers import AccountSer, PasswordSer, UpdateSer
from .models import MyUser

class AccountViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    filter_fields = ['name', 'email', 'role', 'is_staff', 'is_active']
    ordering_fields = ('name', 'email', )
    search_fields = ('name', 'email',)

    def get_permissions(self):
        print(""""Action""")
        print(self.action)
        # if self.action in ['create', 'update', 'list', 'get_other_staff']:
        #     permission_classes = [IsAdminUser]
        if self.action in ['get_doctors', 'retrieve']:
            permission_classes = [IsAdminOrStaff]
        elif self.action == 'reset_password':
            permission_classes = [IsAdminOrIsSelf]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['update']:
            serializer_class = UpdateSer
        elif self.action == 'reset_password':
            serializer_class = PasswordSer # add confirm password
        else:
            serializer_class = AccountSer
        return serializer_class

    def create(self, request):
        serializer = AccountSer(data=request.data)
        if serializer.is_valid():
            user = MyUser(serializer.data)
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'message': 'Account Creation Successful'})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = self.get_object()
        serializer = UpdateSer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Account Update Successful'})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'put'], url_path='reset-password', detail=True)
    def reset_password(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        # add confirm password field to serializer and validators
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'message': 'Password Reset Susseccful'})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
