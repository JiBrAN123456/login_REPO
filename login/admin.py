from django.contrib import admin
from .models import User, Company, Role  # Import your models

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email',  'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')

    def get_company(self, obj):
        return obj.profile.company.name if hasattr(obj, 'profile') and obj.profile.company else None
    get_company.short_description = 'Company'  # Name in the admin panel

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

