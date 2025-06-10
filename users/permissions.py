from rest_framework import permissions


class IsUserPermission(permissions.BasePermission):
    """Checking access rights for users with the "user" role."""

    def has_permission(self, request, view):
        """Checks the user's role."""
        return request.user.role == "user"


class IsManagerPermission(permissions.BasePermission):
    """Checking access rights for users with the "manager" role."""

    def has_permission(self, request, view):
        """Checks the user's role."""
        return request.user.role == "manager"


class IsAdminPermission(permissions.BasePermission):
    """Checking access rights for users with the "admin" role."""

    def has_permission(self, request, view):
        """Checks the user's role."""
        return request.user.role == "admin"


class IsOwnerPermission(permissions.BasePermission):
    """Checking access rights for the user."""

    def has_object_permission(self, request, view, obj):
        """Checks whether the user is an object."""
        return obj == request.user


class IsAuthorOrAdminForUpdateDelete(permissions.BasePermission):
    """
    Only the author can update (PUT/PATCH)
    Only the admin can DELETE
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            return obj.author == request.user
        if request.method == 'DELETE':
            return request.user.role == "manager" or request.user.is_staff
        return True
