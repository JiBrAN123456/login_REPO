from rest_framework.permissions import BasePermission

class HasPermission(BasePermission):
    """
    Custom permission class to check if the user has the required permission.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False  # User must be logged in

        if not hasattr(request.user, 'profile'):
            return False  # Ensure user has a profile

        required_permission = getattr(view, "required_permission", None)
        if required_permission:
            module, action = required_permission.split(".")
            return request.user.profile.has_permission(module, action)

        return True
