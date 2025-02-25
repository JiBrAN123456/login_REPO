from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from simple_history.models import HistoricalRecords
from login.models import Company, User




class VehicleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)  # ✅ Auto-exclude soft-deleted vehicles


# Create your models here.
class Vehicle(models.Model):
    company = models.ForeignKey("login.Company", on_delete=models.CASCADE, related_name="vehicles" )
    created_by = models.ForeignKey("login.User", on_delete=models.CASCADE, null=True, blank=True)
    name  = models.CharField(max_length=50)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    status = models.ForeignKey("InventoryStatus", on_delete=models.SET_NULL, null=True, related_name="vehicles")  # ✅ Status Relationship
    is_deleted = models.BooleanField(default=False)  # ✅ Soft delete feature
    

    objects = VehicleManager()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.brand} {self.model} - {self.year})"
    
class InventoryStatus(models.Model):
     STATUS_CHOICES = [
         ('available','Available'),
         ('sold','Sold'),
         ('reserved','Reserved'),

     ]
     availability = models.CharField(
         max_length=20,
         choices = STATUS_CHOICES,
         default='available',
         unique=True
        
     )

     def __str__(self):
         return self.get_availability_display()
     

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('insurance', 'Insurance'),
        ('registration', 'Registration'),
        ('service_record', 'Service Record'),
        ('other', 'Other'),
    ]

    vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default="other")
    document_file = models.FileField(upload_to="uploads/vehicles/documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Tracks upload date

    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.vehicle.name}"
    


    # ✅ Image Model (Multiple Images per Vehicle)
class VehicleImage(models.Model):
    vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to="uploads/vehicles/images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.vehicle.name}"