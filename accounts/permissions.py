from rest_framework.permissions import BasePermission


class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_doctor


class IsAdminOrIsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff or request.user.is_superuser
