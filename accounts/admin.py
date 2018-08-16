from django.contrib import admin

# Register your models here.
from .models import MyUser

admin.site.register(MyUser)