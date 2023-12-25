from rest_framework.permissions import BasePermission, IsAdminUser


class IsActiveEmployee(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )

    def has_object_permission(self, request, view, obj):
        return obj.supplier == request.user.workplace
