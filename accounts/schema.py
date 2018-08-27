from graphene.relay import Node
from graphene import ObjectType, AbstractType
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
        interfaces = (Node, )


class AccountQuery(AbstractType):
    accounts = DjangoFilterConnectionField(AccountNode)
    account = Node.Field(AccountNode)

    # def resolve_accounts(self, info, **kwargs):
    #     return MyUser.objects.all()
    #
    # def resolve_doctors(self, info, **kwargs):
    #     return MyUser.objects.filter(role='doctor')
    #
    # def resolve_staff(self, info, **kwargs):
    #     return MyUser.objects.exclude(role='doctor')
    #
    # def resolve_account(self, info, **kwargs):
    #     id = kwargs.get('id')
    #     if id is not None:
    #         return MyUser.objects.get(pk=id)
    #     return None