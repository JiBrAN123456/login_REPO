# users/permissions.py

from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if hasattr(user, 'profile') and user.profile.role:
            role = user.profile.role
            # Checking if the role has the necessary permission for the view
            if role.permissions.get(f'can_access_{view.__class__.__name__}', False):
                return True
        return False
