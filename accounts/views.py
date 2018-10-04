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
   HTTP_404_NOT_FOUND, 
   HTTP_400_BAD_REQUEST,
   HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.decorators import action
from .serializers import AccountSer, PasswordSer, UpdateSer
from .models import MyUser

class AccountViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    filter_fields = ['name', 'email', 'role', 'is_staff', 'is_active']
    ordering_fields = ('name', 'email', )
    search_fields = ('name', 'email',)

    # def list(self,request):
    #     accounts = MyUser.objects.exclude(role='doctor');
    #     serializer = self.get_serializer(accounts, many=True);
    #     return Response(serializer.data)
    
    def get_permissions(self):
        print(""""Action""")
        print(self.action)
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
        try: 
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = MyUser(
                    name=serializer.data['name'],
                    email=serializer.data['email'],
                    role=serializer.data['role'],
                    designation=serializer.data['designation'],
                    is_active=serializer.data['is_active'],
                    is_staff=serializer.data['is_staff'],
                    is_superuser=serializer.data['is_superuser'],
                )
                print("Serializer Data")
                print("here" + request.data['password'])
                user.set_password(request.data['password'])
                user.save()
                saved_user = self.get_serializer(user)
                return Response(saved_user.data)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            user = self.get_object()
            serializer = UpdateSer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Account Update Successful'})
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)

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

    @action(methods=['GET'], url_path='doctors', detail=False)
    def get_doctors(self, request):
        doctors = MyUser.objects.filter(role='doctor')
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data)

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': AccountSer(user, context={'request': request}).data
    }