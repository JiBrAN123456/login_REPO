from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Company , Profile
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

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



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a Profile for each new User.
    """
    if created:  # Only create profile if user is new
        Profile.objects.create(user=instance)