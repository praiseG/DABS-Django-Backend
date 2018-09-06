import json
import graphene
from graphene import relay, AbstractType, InputObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from .models import Appointment, Treatment


class AppointmentNode(DjangoObjectType):
    class Meta:
        model = Appointment
        filter_fields = {
            "patient__name": ["icontains", "istartswith", "exact"],
            "patient": ["exact"],
            "status": ["icontains", "istartswith", "exact"],
            "description": ["icontains", ],
        }
        interfaces = (relay.Node, )


class TreatmentNode(DjangoObjectType):
    class Meta:
        model = Treatment
        filter_fields = {
            "appointment__patient": ["exact"],
            "appointment__patient__name": ["icontains", "istartswith", "exact"],
            "diagnosis": ["icontains", "istartswith", "exact"],
        }
        interfaces = (relay.Node, )


class AppointmentCreateInput(InputObjectType):
    STATUSES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('queried', 'Queried'),
    ]
    patient = graphene.Int(required=True)
    logged_by = graphene.Int(required=True)
    description = graphene.String(required=True)
    comment = graphene.String()
    assigned_to = graphene.Int(required=True)
    status = graphene.Enum('status', STATUSES)


class TreatmentCreateInput(InputObjectType):
    appointment = graphene.Int(required=True)
    diagnosis = graphene.String(required=True) # text field for graphene
    prescription = graphene.String(required=True)


class CreateAppointmentMutation(relay.ClientIDMutation):
    class Input:
        appointment = graphene.Argument(AppointmentCreateInput)

    status = graphene.Int()
    errors = graphene.String()
    appointment = graphene.Field(AppointmentNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        if not context.user.is_authenticated():
            return cls(status=403)
        appt_data = args.get('appointment')
        appt_data['logged_by'] = context.user
        obj = Appointment.objects.create(**appt_data)
        return cls(status=200, appointment=obj)


class CreateTreatmentMutation(relay.ClientIDMutation):
    class Input:
        treatment = graphene.Field(TreatmentCreateInput)

    status = graphene.Int()
    errors = graphene.String()
    treatment = graphene.Field(TreatmentNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        if not context.user.is_authenticated():
            return cls(status=403)
        tdata = args.get('treatment')
        obj = Treatment.objects.create(**tdata)
        return cls(status=200, treatment=obj)


class AppointMentQuery(AbstractType):
    appointment = relay.Node.Field(AppointmentNode)
    appointments = DjangoFilterConnectionField(AppointmentNode)

    treatment = relay.Node.Field(TreatmentNode)
    treatments = DjangoFilterConnectionField(TreatmentNode)


class AppointmentMutations(AbstractType):
    create_appointment = CreateAppointmentMutation.Field()
    create_treatment = CreateTreatmentMutation.Field()
