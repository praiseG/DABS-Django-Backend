from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import(
    HTTP_404_NOT_FOUND, 
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from .permissions import IsStaffWithRole
from .serializers import PatientSer
from appointments.serializers import AppointmentSer, TreatmentSer
from .models import Patient
from appointments.models import Appointment, Treatment


class PatientViewset(ModelViewSet):
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

    def get_serializer_class(self):
        if self.action == 'get_appointments':
            serializer_class = AppointmentSer
        elif self.action == 'get_history':
            serializer_class = TreatmentSer
        else:
            serializer_class = PatientSer
        return serializer_class

    def create(self, request, *args, **kwargs): #registered_by
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                patient = Patient(
                    name=serializer.data['name'],
                    email=serializer.data['email'],
                    mobile=serializer.data['mobile'],
                    age=serializer.data['age'],
                    address=serializer.data['address'],
                    disability=serializer.data['disability'],
                )
                patient.registered_by = request.user
                patient.save()
                serialized = self.get_serializer(patient)
                return Response(serialized.data)
            return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("e here")
            print(e)
            print(type(e))
            return Response({'error': str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=True, url_path='appointments')
    def get_appointments(self, request, pk=None):
        patient = self.get_object()
        appointments = Appointment.objects.filter(patient=patient)
        if appointments:
            serializer = self.get_serializer(appointments, many=True)
            return Response(serializer.data)
        return Response({"details": "No Appointments found for selected Patient"}, status=HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=True, url_path='history')
    def get_history(self, request, pk=None):
        patient = self.get_object()
        treatments = Treatment.objects.filter(appointment__patient=patient)
        if treatments:
            serializer= self.get_serializer(treatments, many=True)
            return Response(serializer.data)
        return Response({"details": "No History Found for selected Patient"}, status=HTTP_404_NOT_FOUND)