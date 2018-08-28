from django.contrib import admin
from .models import Patient
# Register your models here.


class PatientModelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'mobile',
        'age',
        'disability',
        'registered_by',
        'registered_on',
    )
    search_fields = ('name', 'email', 'mobile', )
    ordering = ('registered_on', 'name', 'email', )

admin.site.register(Patient, PatientModelAdmin)
