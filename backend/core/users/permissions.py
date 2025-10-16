from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an account or admin to access/modify it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin permissions
        if request.user.is_staff:
            return True
            
        # Instance must have an attribute named `user`
        return obj.id == request.user.id

class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow non-authenticated users to access.
    Useful for registration endpoints.
    """
    def has_permission(self, request, view):
        return not request.user.is_authenticated

class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow super admins to access.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser