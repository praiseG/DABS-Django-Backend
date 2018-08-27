import graphene
import graphql_jwt
from accounts.schema import AccountQuery


class RootQuery(AccountQuery, graphene.ObjectType):
    pass


class RootMutation(graphene.ObjectType):
    auth_token = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()

schema = graphene.Schema(query=RootQuery, mutation=RootMutation,  auto_camelcase=False)