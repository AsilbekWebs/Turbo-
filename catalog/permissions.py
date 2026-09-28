from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_admin(user):
    return bool(
        user
        and user.is_authenticated
        and (user.is_staff or getattr(user, 'role', None) == 'admin')
    )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return is_admin(request.user)


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return is_admin(request.user)