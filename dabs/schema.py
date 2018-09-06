from graphene import Schema, ObjectType
import graphql_jwt
from accounts.schema import AccountQuery, AccountMutations
from appointments.schema import AppointMentQuery, AppointmentMutations
from patients.schema import PatientQuery, PatientMutations


class RootQuery(
    AccountQuery,
    AppointMentQuery,
    PatientQuery,
    ObjectType
):
    pass


class RootMutation(
    AccountMutations,
    PatientMutations,
    AppointmentMutations,
    ObjectType
):
    auth_token = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()

schema = Schema(query=RootQuery, mutation=RootMutation,  auto_camelcase=False)