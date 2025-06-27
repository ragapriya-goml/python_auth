
from django.db import models
from django.conf import settings
from rest_framework.permissions import BasePermission

#MODELS

class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Permission(models.Model):
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.codename

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')

class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_users')

    class Meta:
        unique_together = ('user', 'role')

#PERMISSIONS
class HasRolePermission(BasePermission):
    """
    DRF permission class that checks whether the user has any of the required roles
    defined on the view as `required_roles = ['admin', 'editor']`.
    """

    def has_permission(self, request, view):
        print(f"DEBUG HasRolePermission: User: {request.user}")
        print(f"DEBUG HasRolePermission: Is authenticated: {request.user.is_authenticated}")
        
        required_roles = getattr(view, 'required_roles', [])
        print(f"DEBUG HasRolePermission: Required roles: {required_roles}")

        if not request.user or not request.user.is_authenticated:
            print("DEBUG HasRolePermission: User not authenticated, denying access")
            return False

        user_roles = UserRole.objects.filter(user=request.user, role__name__in=required_roles)
        user_role_names = [ur.role.name for ur in user_roles]
        print(f"DEBUG HasRolePermission: User roles: {user_role_names}")
        
        has_role = user_roles.exists()
        print(f"DEBUG HasRolePermission: Has required role: {has_role}")
        return has_role

class HasPermissionCodename(BasePermission):
    """
    DRF permission class to check if the user has a specific permission codename
    defined as `required_permissions = ['can_view_reports']` on the view.
    """

    def has_permission(self, request, view):
        print(f"DEBUG HasPermissionCodename: User: {request.user}")
        print(f"DEBUG HasPermissionCodename: Is authenticated: {request.user.is_authenticated}")
        
        required_perms = getattr(view, 'required_permissions', [])
        print(f"DEBUG HasPermissionCodename: Required permissions: {required_perms}")

        if not request.user or not request.user.is_authenticated:
            print("DEBUG HasPermissionCodename: User not authenticated, denying access")
            return False

        user_roles = Role.objects.filter(role_users__user=request.user)
        print(f"DEBUG HasPermissionCodename: User roles: {[role.name for role in user_roles]}")
        
        user_permissions = Permission.objects.filter(rolepermission__role__in=user_roles)
        print(f"DEBUG HasPermissionCodename: User permissions: {[perm.codename for perm in user_permissions]}")

        has_permission = user_permissions.filter(codename__in=required_perms).exists()
        print(f"DEBUG HasPermissionCodename: Has required permission: {has_permission}")
        
        return has_permission

