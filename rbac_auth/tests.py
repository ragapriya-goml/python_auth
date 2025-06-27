from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from models import Role, RolePermission, UserRole, Permission

User = get_user_model()

class RBACPermissionTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john', password='test123')
        self.role = Role.objects.create(name='admin')
        self.permission = Permission.objects.create(codename='can_view_reports')
        RolePermission.objects.create(role=self.role, permission=self.permission)
        UserRole.objects.create(user=self.user, role=self.role)

        # Get JWT Token
        response = self.client.post('/auth/login/', {
            'username': 'john',
            'password': 'test123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_admin_role_grants_access(self):
        response = self.client.get('/admin-only/')
        self.assertEqual(response.status_code, 200)

    def test_permission_grants_access(self):
        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_blocked(self):
        self.client.credentials()  # Remove token
        response = self.client.get('/admin-only/')
        self.assertEqual(response.status_code, 401)
