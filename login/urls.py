from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterUserView, LoginView, ProfileView, CompanyListCreateView, CompanyDetailView, RoleListCreateView, RoleDetailView, MenuListCreateView, RoleMenuPermissionsListCreateView

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('companies/', CompanyListCreateView.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('roles/', RoleListCreateView.as_view(), name='role-list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('menus/', MenuListCreateView.as_view(), name='menu-list'),
    path('permissions/', RoleMenuPermissionsListCreateView.as_view(), name='permissions-list'),
]
