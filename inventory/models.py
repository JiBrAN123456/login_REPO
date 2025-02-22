from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from simple_history.models import HistoricalRecords

# Create your models here.
class Vehicle(models.Model):
    name  = models.CharField(max_length=50)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    

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