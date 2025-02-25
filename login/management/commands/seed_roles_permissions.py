from django.core.management.base import BaseCommand
from login.models import Role, Menu, RoleMenuPermissions, User, Company, Domain
from django.contrib.auth import get_user_model



class Command(BaseCommand):
    help = "Seeds roles and permissions"

    def handle(self, *args, **options):
        # Ensure there's a default company
        company, created = Company.objects.get_or_create(
            name="Default Company",
            schema_name="default"
        )

        # Ensure there's a domain for the company
        domain, _ = Domain.objects.get_or_create(
            domain="default.example.com",
            tenant=company,  # Assign the company as the tenant
            is_primary=True
        )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded domain {domain.domain}"))

        # 🚀 Step 1: Create Menus
        menu_items = ["Dashboard", "Users", "Vehicles", "Finance", "Sales", "Reports", "Settings"]
        for menu_name in menu_items:
            menu, created = Menu.objects.get_or_create(menu_name=menu_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created menu: {menu_name}"))

        # 🚀 Step 2: Create Roles for the Company
        roles_data = [
            {"name": "Admin"},
            {"name": "Manager"},
            {"name": "Salesperson"},
        ]
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(name=role_data["name"], company=company)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created role: {role.name} for {company.name}"))

        # 🚀 Step 3: Assign Role Permissions
        role_permissions = {
            "Admin": {
                "Dashboard": ["view"], "Users": ["view", "add", "edit", "delete"],
                "Vehicles": ["view", "add", "edit", "delete"], "Finance": ["view", "edit"],
                "Sales": ["view", "edit"], "Reports": ["view"], "Settings": ["view", "edit"]
            },
            "Manager": {
                "Dashboard": ["view"], "Users": ["view", "edit"], "Vehicles": ["view", "add", "edit"],
                "Finance": ["view"], "Sales": ["view"], "Reports": ["view"], "Settings": []
            },
            "Salesperson": {
                "Dashboard": ["view"], "Users": [], "Vehicles": ["view"],
                "Finance": [], "Sales": ["view", "add"], "Reports": [], "Settings": []
            },
        }

        for role_name, permissions in role_permissions.items():
            role = Role.objects.get(name=role_name, company=company)  # Fetch role for the correct company
            for menu_name, actions in permissions.items():
                menu = Menu.objects.get(menu_name=menu_name)
                role_permission, created = RoleMenuPermissions.objects.get_or_create(
                    role=role, menu=menu,
                    defaults={
                        "can_view": "view" in actions,
                        "can_add": "add" in actions,
                        "can_edit": "edit" in actions,
                        "can_delete": "delete" in actions,
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ Assigned {actions} permissions to {role_name} for {menu_name} in {company.name}"))

        # 🚀 Step 4: Create Superuser for the Default Company
        User = get_user_model()
        email = "admin@example.com"
        if not User.objects.filter(email=email).exists():
            superuser = User.objects.create_superuser(email=email, password="Admin@123", company=company)
            self.stdout.write(self.style.SUCCESS(f"✅ Superuser created: {email} under {company.name}"))

        self.stdout.write(self.style.SUCCESS("🚀 Seeding completed successfully!"))
