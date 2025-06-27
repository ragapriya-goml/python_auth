from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rbac_auth.views import AdminOnlyView, ReportView, DashboardView, EditContentView, SettingsView

urlpatterns = [
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin-only/", AdminOnlyView.as_view(), name="admin_only"),
    path("reports/", ReportView.as_view(), name="report_view"),
     path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('reports/', ReportView.as_view(), name='reports'),
    path('edit-content/', EditContentView.as_view(), name='edit-content'),
    path('settings/', SettingsView.as_view(), name='settings'),
]
