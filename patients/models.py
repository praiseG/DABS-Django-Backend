from django.db import models


class Patient(models):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    age = models.IntegerField()
    height = models.CharField(max_length=10)
    mobile = models.CharField(max_length=30, unique=True)
    disability = models.CharField(max_length=255, blank=True, null=True)
    chronical_diseases = models.CharField(max_length=255, blank=True, null=True)
