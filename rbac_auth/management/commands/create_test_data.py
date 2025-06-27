from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Role, Permission, RolePermission, UserRole


class Command(BaseCommand):
    help = 'Create test data for RBAC system'

    def handle(self, *args, **options):
        # Create roles
        admin_role, _ = Role.objects.get_or_create(name='admin', defaults={'description': 'Administrator role'})
        editor_role, _ = Role.objects.get_or_create(name='editor', defaults={'description': 'Editor role'})
        viewer_role, _ = Role.objects.get_or_create(name='viewer', defaults={'description': 'Viewer role'})

        # Create permissions
        can_view_reports, _ = Permission.objects.get_or_create(
            codename='can_view_reports', 
            defaults={'description': 'Can view reports'}
        )
        can_view_dashboard, _ = Permission.objects.get_or_create(
            codename='can_view_dashboard', 
            defaults={'description': 'Can view dashboard'}
        )
        can_edit_content, _ = Permission.objects.get_or_create(
            codename='can_edit_content', 
            defaults={'description': 'Can edit content'}
        )
        can_manage_settings, _ = Permission.objects.get_or_create(
            codename='can_manage_settings', 
            defaults={'description': 'Can manage settings'}
        )

        # Assign permissions to roles
        RolePermission.objects.get_or_create(role=admin_role, permission=can_view_reports)
        RolePermission.objects.get_or_create(role=admin_role, permission=can_view_dashboard)
        RolePermission.objects.get_or_create(role=admin_role, permission=can_edit_content)
        RolePermission.objects.get_or_create(role=admin_role, permission=can_manage_settings)

        RolePermission.objects.get_or_create(role=editor_role, permission=can_view_dashboard)
        RolePermission.objects.get_or_create(role=editor_role, permission=can_edit_content)

        RolePermission.objects.get_or_create(role=viewer_role, permission=can_view_dashboard)

        # Create test users
        admin_user, created = User.objects.get_or_create(
            username='admin', 
            defaults={'email': 'admin@test.com', 'is_staff': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        editor_user, created = User.objects.get_or_create(
            username='editor', 
            defaults={'email': 'editor@test.com'}
        )
        if created:
            editor_user.set_password('editor123')
            editor_user.save()

        viewer_user, created = User.objects.get_or_create(
            username='viewer', 
            defaults={'email': 'viewer@test.com'}
        )
        if created:
            viewer_user.set_password('viewer123')
            viewer_user.save()

        # User without any role
        norole_user, created = User.objects.get_or_create(
            username='norole', 
            defaults={'email': 'norole@test.com'}
        )
        if created:
            norole_user.set_password('norole123')
            norole_user.save()

        # Assign roles to users
        UserRole.objects.get_or_create(user=admin_user, role=admin_role)
        UserRole.objects.get_or_create(user=editor_user, role=editor_role)
        UserRole.objects.get_or_create(user=viewer_user, role=viewer_role)

        self.stdout.write(self.style.SUCCESS('Successfully created test data!'))
        self.stdout.write('Test users created:')
        self.stdout.write('- admin/admin123 (admin role - all permissions)')
        self.stdout.write('- editor/editor123 (editor role - dashboard, edit content)')
        self.stdout.write('- viewer/viewer123 (viewer role - dashboard only)')
        self.stdout.write('- norole/norole123 (no role - no permissions)')
