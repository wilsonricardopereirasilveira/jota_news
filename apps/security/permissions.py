from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEditor(BasePermission):
    """Allow access only to staff/editor users."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class ReadOnly(BasePermission):
    """Allow only safe method requests."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
