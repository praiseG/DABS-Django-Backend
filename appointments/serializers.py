from rest_framework import serializers
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
)

from .models import Appointment