from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django_tenants.models import TenantMixin, DomainMixin
from simple_history.models import HistoricalRecords
import uuid
from django.core.exceptions import ValidationError


# 🚀 Domain Model (for Subdomains)
class Domain(DomainMixin):
    pass

# 🚀 Multi-Tenant Company Model
class Company(TenantMixin):
    id = models.BigAutoField(primary_key=True)
    company_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    schema_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(default="Not Provided")
    is_active = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True,  related_name="companies_created")
    modified_by = models.ForeignKey('User', on_delete=models.SET_NULL,  null=True, blank=True, related_name="companies_modified")
    
    auto_create_schema = True  # Automatically creates a separate schema
    auto_drop_schema = True 

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if it's a new instance
        super().save(*args, **kwargs)  # Save the company first

        if is_new:
            with transaction.atomic():
                Domain.objects.create(
                    domain=f"{self.schema_name}.yourapp.com",
                    tenant=self,
                    is_primary=True
                )


    def __str__(self):
        return self.name
    



from django.core.management import CommandError

# 🚀 Multi-Tenant User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email required")

        email = self.normalize_email(email)

        # Ensure normal users have a company
        if not extra_fields.get("is_superuser", False) and not extra_fields.get("company"):
            raise ValueError("Normal users must be assigned a company.")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
       extra_fields.setdefault("is_staff", True)
       extra_fields.setdefault("is_superuser", True)

       if "username" not in extra_fields or not extra_fields["username"]:
           extra_fields["username"] = email.split("@")[0]  # Use email prefix as username

       return self.create_user(email, password, **extra_fields)

# 🚀 Multi-Tenant User Model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    user_guid = models.UUIDField(default=uuid.uuid4, unique=True,editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(unique=True, max_length= 15, blank= True, null = True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, blank=True, related_name="users")
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def clean(self):
    # Normal users must have a company, but superusers don't need one
       if not self.is_superuser and self.company is None:
          raise ValidationError("Normal users must be assigned a company.")
       super().clean()


    def __str__(self):
        return self.email


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="roles")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name="roles_created")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True ,related_name="roles_modified")
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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="permissions_created")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name="permissions_modified")
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['role', 'menu'], name="unique_role_menu_permission")
        ]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def has_permission(self, module, action):
        """
        Check if the user has permission for a specific action on a module (menu).
        """
        if not self.role:
            return False  # User must have a role to check permissions

        try:
            role_permission = RoleMenuPermissions.objects.filter().first(role=self.role, menu__menu_name=module)
            return getattr(role_permission, f"can_{action}", False)  # Check if action is allowed
        except RoleMenuPermissions.DoesNotExist:
            return False  # No permissions found, deny access
