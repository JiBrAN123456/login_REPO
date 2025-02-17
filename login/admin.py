from django.contrib import admin
from .models import User, Company, Role, Profile  # Import your models

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'company', 'is_staff', 'is_active', 'created_at')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active', 'company')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Make sure 'bio' field is valid or remove it
    search_fields = ('user__email',)
