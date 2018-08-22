from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
   AllowAny,
   # IsAdminUser, IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.status import (
   HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
)
from rest_framework.decorators import action
from .serializers import AccountSer, PasswordSer
from .models import MyUser


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSer
    # permission_classes = [AllowAny]
    queryset = MyUser.objects.all()

    def create(self, request):
        serializer = AccountSer(data=request.data)
        if serializer.is_valid():
            user = MyUser(serializer.data)
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'message': 'Account Created Successfully'})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # add permission IsAdminorIsSelf
    @action(methods=['post'], detail=True)
    def reset_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'message': 'Password Reset Susseccful'})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
