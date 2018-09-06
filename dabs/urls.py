"""dabs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.views import AccountViewSet
from patients.views import PatientViewset
from appointments.views import AppointmentViewSet
# DRF Routes
router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'patients', PatientViewset)
router.register(r'appointments', AppointmentViewSet, base_name='appointment')


# GraphQL Route
class DabGraphQLView(LoginRequiredMixin, GraphQLView):
    pass

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth-api/', include('rest_framework.urls')),
    url(r'^api/auth/token/', obtain_jwt_token),
    url(r'^api/refresh/token/', refresh_jwt_token),
    url(r'^api/verify/token/', verify_jwt_token),
    url(r'^api/v1/', include(router.urls)),
    # url(r'^api/v2/', csrf_exempt(DabGraphQLView.as_view(graphiql=True))),
    url(r'^api/v2/', csrf_exempt(GraphQLView.as_view(batch=True))),
    url(r'^gql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
