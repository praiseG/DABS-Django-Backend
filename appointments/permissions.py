from rest_framework.permissions import BasePermission
from patients.permissions import IsStaffWithRole


class IsAssignedDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_doctor and request.user == obj.assigned_to


class IsAppointmentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_doctor and request.user == obj.appointment.assigned_to


class IsHelpdesk(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'helpdesk'


class IsStaffOrAssignedDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsStaffWithRole.has_object_permission or IsAssignedDoctor.has_object_permission


class IsHelpdeskOrAssignedDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'helpdesk' or IsAssignedDoctor.has_object_permission