from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin,
)
from rest_framework.permissions import (
   AllowAny,
   IsAdminUser,IsAuthenticated
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


# uses custom  viewset to leave out Destroy action
class AccountViewSet(ListModelMixin,
                     RetrieveModelMixin,
                     CreateModelMixin,
                     UpdateModelMixin,
                     GenericViewSet
                     ):
    queryset = MyUser.objects.all()

    def get_permissions(self):
        print(""""Action""")
        print(self.action)
        if self.action in ['create', 'update', 'list', 'get_other_staff']:
            permission_classes = [IsAdminUser]
        elif self.action in ['get_doctors', 'retrieve']:
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
        serializer = PasswordSer(data=request.data)
        # add confirm password field to serializer and validators
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'message': 'Password Reset Susseccful'})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='doctors', detail=False)
    def get_doctors(self, request):
        try:
            doctors = MyUser.objects.filter(role='doctor')
            serializer = AccountSer(doctors, many=True, context={'request': request})
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'message':'There are no Doctors Found'}, status=HTTP_404_NOT_FOUND)

    @action(methods=['get'], url_path='staff', detail=False)
    def get_other_staff(self, request):
        try:
            staff = MyUser.objects.exclude(role='doctor')
            serializer = AccountSer(staff, many=True, context={'request': request})
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'There are no Non-Doctor Staff Found'}, status=HTTP_404_NOT_FOUND)