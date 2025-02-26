from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterUserView, LoginView, ProfileView,
    CompanyListCreateView, CompanyDetailView,
    RoleListCreateView, RoleDetailView,
    MenuListCreateView,
    RoleMenuPermissionsListCreateView,
    debug_view
)

urlpatterns = [
    # Debug Route
    path('debug/', debug_view, name='debug'),

    # Authentication Routes
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),

    # Company Management Routes
    path('companies/', CompanyListCreateView.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    # Role Management Routes
    path('roles/', RoleListCreateView.as_view(), name='role-list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),

    # Menu Management Routes
    path('menus/', MenuListCreateView.as_view(), name='menu-list'),

    # Role Menu Permissions Routes
    path('permissions/', RoleMenuPermissionsListCreateView.as_view(), name='permissions-list'),
]
