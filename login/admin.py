from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company, Role
from django_tenants.utils import tenant_context  # Required for tenant handling

@admin.register(User)
class UserAdmin(BaseUserAdmin):  # Extends Django's built-in UserAdmin
    list_display = ('email', 'is_active', 'is_staff', 'get_company')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)

    def get_queryset(self, request):
        """Restrict visibility of users based on tenant"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers see all users
        elif hasattr(request.user, 'profile') and request.user.profile.company:
            return qs.filter(profile__company=request.user.profile.company)
        return qs.none()  # If no company, return empty

    def get_company(self, obj):
        """Display company name in admin list"""
        return obj.profile.company.name if hasattr(obj, 'profile') and obj.profile.company else None
    get_company.short_description = 'Company'  

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'is_active')
    search_fields = ('name', 'schema_name')
    ordering = ('name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
