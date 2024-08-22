# users/permissions.py

from django.core.exceptions import PermissionDenied
from .models import UserRole, RolePermission, Permission

class Security:
    @staticmethod
    def secureAccess(permission_code, user_id):
        try:
            # Correct field name from permission_codename to permission_code
            permission = Permission.objects.get(permission_code=permission_code)
            role_permissions = RolePermission.objects.filter(permission=permission)
            user_roles = UserRole.objects.filter(user_id=user_id, role__in=[rp.role for rp in role_permissions])
            if not user_roles.exists():
                raise PermissionDenied("You are restricted from accessing this service")
            return True
        except Permission.DoesNotExist:
            raise PermissionDenied("You are restricted from accessing this service")
