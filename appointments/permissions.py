from rest_framework.permissions import BasePermission


class IsAssignedDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_doctor and request.user == obj.assigned_to


class IsAppointmentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_doctor and request.user == obj.appointment.assigned_to