import graphene
from graphene import relay, AbstractType, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import  DjangoFilterConnectionField
from .models import Patient


class PatientNode(DjangoObjectType):
    class Meta:
        model = Patient
        filter_fields = {
            "name": ["icontains", "istartswith", "exact"],
            "email": ["icontains", "istartswith", "exact"],
        }
        interfaces = (relay.Node, )


class PatientCreateInput(InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    address = graphene.String(required=True)
    age = graphene.Int(required=True)
    mobile = graphene.String(required=True)
    disability = graphene.String()


class CreatePatientMutation(relay.ClientIDMutation):
    class Input:
        patient = graphene.Argument(PatientCreateInput)

    status = graphene.Int()
    errors = graphene.String()
    new_patient = graphene.Field(PatientNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        if not context.user.is_authenticated():
            return cls(status=403)
        patient_data = args.get('patient')
        patient_data['registered_by'] = context.user
        obj = Patient.objects.create(**patient_data)
        return cls(status=200, new_patient=obj)


class PatientQuery(AbstractType):
    patient = relay.Node.Field(PatientNode)
    patients = DjangoFilterConnectionField(PatientNode)


class PatientMutations(AbstractType):
    create_patient = CreatePatientMutation.Field()



