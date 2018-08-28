from rest_framework.permissions import BasePermission


class IsStaffWithRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.role is not None and request.user.role != 'doctor'