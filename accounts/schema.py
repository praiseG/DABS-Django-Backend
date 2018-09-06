import json
import graphene
from graphene import relay, AbstractType, InputObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from .models import MyUser


class AccountNode(DjangoObjectType):
    class Meta:
        model = MyUser
        exclude_fields = ('password', )
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'email':  ['exact', 'icontains'],
            'role': ['exact'],
        }
        # filter_fields = ['role', 'name', 'email']
        interfaces = (relay.Node, )


class AccountUpdateInput(InputObjectType):
    ROLES = [
        ('doctor', 'Doctor'),
        ('helpdesk', 'Helpdesk'),
        ('manager', 'Manager')
    ]
    email = graphene.String(required=True)
    name = graphene.String(required=True)
    designation = graphene.String(required=True)
    role = graphene.Enum('role', ROLES)
    is_staff = graphene.Boolean()
    is_superuser = graphene.Boolean()
    is_active = graphene.Boolean()


class ResetPasswordInput(InputObjectType):
    password1 = graphene.String(required=True)
    password2 = graphene.String(required=True)


class AccountCreateInput(
    AccountUpdateInput,
    ResetPasswordInput,
    InputObjectType
):
    pass

# class AccountCreateInput(InputObjectType):
#     email = graphene.String(required=True)
#     name = graphene.String(required=True)
#     designation = graphene.String(required=True)
#     password = graphene.String(required=True)
#     password2 = graphene.String(required=True)
#     role = graphene.String()
#     is_staff = graphene.Boolean()
#     is_superuser = graphene.Boolean()
#     is_active = graphene.Boolean()


class CreateAccountMutation(relay.ClientIDMutation):
    class Input:
        account = graphene.Argument(AccountCreateInput)

    status = graphene.Int()
    errors = graphene.String()
    new_account = graphene.Field(AccountNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        if not context.user.is_authenticated():
            return cls(status=403)
        user_data = args.get('account')
        password1 = user_data['password1']
        password2 = user_data['password2']
        if password2 != password1:
            return cls(status=400, errors=json.dumps({"detail":"Passwords do not match"}))
        obj = MyUser.objects.create(**user_data)
        obj.set_password(password1)
        obj.save()
        return cls(status=200, new_account=obj)


class AccountQuery(AbstractType):
    accounts = DjangoFilterConnectionField(AccountNode)
    account = relay.Node.Field(AccountNode)


class AccountMutations(AbstractType):
    create_account = CreateAccountMutation.Field()