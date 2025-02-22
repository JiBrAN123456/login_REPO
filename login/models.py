from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django_tenants.models import TenantMixin, DomainMixin
from simple_history.models import HistoricalRecords
import uuid


# 🚀 Domain Model (for Subdomains)
class Domain(DomainMixin):
    pass

# 🚀 Multi-Tenant Company Model
class Company(TenantMixin):
    id = models.BigAutoField(primary_key=True)
    company_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    schema_name = models.CharField(max_length=100, unique=True, default="public")
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="companies_created")
    modified_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="companies_modified")


    auto_create_schema = True  # Automatically creates a separate schema
    auto_drop_schema = True 

    def __str__(self):
        return self.name
    




# 🚀 Multi-Tenant User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email required")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)



# 🚀 Multi-Tenant User Model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    user_guid = models.UUIDField(default=uuid.uuid4, unique=True,editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="users")
    role = models.ForeignKey('Role',on_delete=models.SET_NULL, null=True)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()


    def __str__(self):
        return self.email


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="roles")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="roles_created")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="roles_modified")
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Menu(models.Model):
    id = models.BigAutoField(primary_key=True)
    menu_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.menu_name


class RoleMenuPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="permissions")
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="permissions_created")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="permissions_modified")
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('role', 'menu')  # Ensures no duplicate role-menu permissions
