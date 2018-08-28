from django.db import models
from accounts.models import MyUser


class Patient(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=50, unique=True)
    address = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    mobile = models.CharField(max_length=30, unique=True)
    disability = models.CharField(max_length=255, blank=True, null=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    registered_by = models.ForeignKey(MyUser, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.name)