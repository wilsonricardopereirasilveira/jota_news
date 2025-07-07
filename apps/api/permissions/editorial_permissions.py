from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEditorOrReadOnly(BasePermission):
    """Allow read-only access for anyone, write for staff users."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_staff)
