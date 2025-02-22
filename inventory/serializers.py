from rest_framework import serializers
from .models import Vehicle, InventoryStatus, Document

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"

class InventoryStatusSerializer(serializers.ModelSerializer):
     status_name_display = serializers.CharField(source="get_availability_display", read_only=True)  
    
    class Meta:
        model = InventoryStatus
        fields = "__all__"

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"




