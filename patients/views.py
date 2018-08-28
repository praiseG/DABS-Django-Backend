from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .permissions import IsStaffWithRole
from .serializers import PatientSer
from .models import Patient
from appointments.models import Appointment, Treatment


class PatientViewset(ListModelMixin,
                     CreateModelMixin,
                     UpdateModelMixin,
                     RetrieveModelMixin, GenericViewSet):
    serializer_class = PatientSer
    queryset = Patient.objects.all()
    filter_fields = ('name', 'email', 'mobile', )
    ordering_fields = ('name', 'email', )
    search_fields = ('name', 'email', 'mobile')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsStaffWithRole]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # def get_serializer_class(self):
    #     pass

    @action(methods=['GET'], detail=True, url_path='appointments')
    def get_appointments(self, request, pk=None):
        # try seriaizr.is_valid(raise_exception=True)
        pass #get all patient past appointments

    @action(methods=['GET'], detail=True, url_path='history')
    def get_history(self, request, pk=None):
        pass # get past diagnosis