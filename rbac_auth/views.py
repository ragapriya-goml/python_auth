from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import HasRolePermission, HasPermissionCodename


# ✅ Role-based view (e.g. only admin role can access)
class AdminOnlyView(APIView):
    required_roles = ['admin']
    permission_classes = [IsAuthenticated, HasRolePermission]

    def get(self, request):
        return Response({'message': 'Hello Admin!'})


# ✅ Permission-based views

class DashboardView(APIView):
    required_permissions = ['can_view_dashboard']
    permission_classes = [IsAuthenticated, HasPermissionCodename]

    def get(self, request):
        return Response({'message': 'Welcome to the dashboard!'})


class ReportView(APIView):
    required_permissions = ['can_view_reports']
    permission_classes = [IsAuthenticated, HasPermissionCodename]

    def get(self, request):
        return Response({'message': 'Access granted to reports.'})


class EditContentView(APIView):
    required_permissions = ['can_edit_content']
    permission_classes = [IsAuthenticated, HasPermissionCodename]

    def get(self, request):
        return Response({'message': 'You have edit access to content.'})


class SettingsView(APIView):
    required_permissions = ['can_manage_settings']
    permission_classes = [IsAuthenticated, HasPermissionCodename]

    def get(self, request):
        return Response({'message': 'You can manage system settings.'})
