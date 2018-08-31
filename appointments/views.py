from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from patients.permissions import IsStaffWithRole
from .serializers import (
    AppointmentSer,
    AppointmentLogSer,
    TreatmentSer,
)
from .permissions import (
    IsHelpdesk,
    IsAppointmentOwner,
    IsStaffOrAssignedDoctor,
    IsHelpdeskOrAssignedDoctor
)
from .models import Appointment, Treatment


class AppointmentViewSet(ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_doctor:
            return Appointment.objects.filter(assigned_to=self.request.user)
        return Appointment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            serializer_class = AppointmentLogSer
        elif self.action == 'get_treatment':
            serializer_class = TreatmentSer
        else:
            serializer_class = AppointmentSer
        return serializer_class

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsHelpdesk]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsHelpdeskOrAssignedDoctor]
        else:
            permission_classes = [IsStaffOrAssignedDoctor]
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=True, url_path='treatment')
    def get_treatment(self, request, pk=None):
        appointment = self.get_object()
        try:
            treatment = Treatment.objects.get(appointment=appointment)
            serializer = self.get_serializer(treatment)
            return Response(serializer.data)
        except Treatment.DoesNotExist:
            return Response({'detail': 'No Treatment Found for selected Appointment'}, status=HTTP_404_NOT_FOUND)


class TreatmentViewSet(CreateModelMixin,
                       UpdateModelMixin,
                       GenericViewSet):
    serializer_class = TreatmentSer
    queryset = Treatment.objects.all()
    permission_classes = [IsAppointmentOwner]