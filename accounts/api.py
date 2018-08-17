from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import (
   AllowAny,
   # IsAdminUser, IsAuthenticated,
)
from .serializers import AccountSer
from .models import MyUser


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSer
    permission_classes = AllowAny
    queryset = MyUser.objects.all()