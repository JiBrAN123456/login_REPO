from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Company
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_migrate)
def create_default_company(sender, **kwargs):
    if sender.name == "login":  # Ensures it only runs for this app
        if not Company.objects.filter(schema_name="public").exists():
            user = User.objects.first()  # Assign to first user or set to None
            Company.objects.create(
                name="Default Company",
                schema_name="public",
                address="Default Address",
                created_by=user,
                modified_by=user
            )
