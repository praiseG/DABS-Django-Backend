from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.decorators import action
from patients.permissions import IsStaffWithRole
from .serializers import (
    AppointmentSer,
    AppointmentLogSer,
    TreatmentSer,
)
from .permissions import IsAssignedDoctor, IsAppointmentOwner
from accounts.permissions import IsAdminOrStaff
from .models import Appointment, Treatment


class AppointmentViewSet(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         GenericViewSet
                         ):

    def get_queryset(self):
        if self.request.user.is_doctor:
            return Appointment.objects.filter(assigned_to=self.request.user)
        return Appointment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            serializer_class = AppointmentLogSer
        else:
            serializer_class = AppointmentSer
        return serializer_class

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsStaffWithRole]
        elif self.action in ['update', 'get_treatment']:
            permission_classes = [IsStaffWithRole, IsAssignedDoctor]
        else:
            permission_classes = [IsAdminOrStaff, IsAssignedDoctor]
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=True, url_path='treatment')
    def get_treatment(self, request, pk=None):
        appointment = self.get_object()
        return Treatment.objects.filter(appointment=appointment)


class TreatmentViewSet(CreateModelMixin,
                       UpdateModelMixin,
                       GenericViewSet):
    serializer_class = TreatmentSer
    queryset = Treatment.objects.all()
    permission_classes = [IsAppointmentOwner]