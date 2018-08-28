from django.contrib import admin

# Register your models here.
from .models import Appointment, Treatment

class AppointmentModelAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'logged_by',
        'assigned_to',
        'description',
        'logged_at',
        'status',
    )
    list_filter = ('status', )
    search_fields = ('patient', 'assigned_to')
    ordering = ('logged_at', )


class TreatmentModelAdmin(admin.ModelAdmin):
    list_display = (
        'appointment',
        'diagnosis',
        'prescription',
    )


admin.site.register(Appointment, AppointmentModelAdmin)
admin.site.register(Treatment, TreatmentModelAdmin)