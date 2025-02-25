from rest_framework import serializers
from .models import Vehicle, InventoryStatus, Document , VehicleImage
from login.models import Company, User


class VehicleSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    
    
    class Meta:
        model = Vehicle
        fields = "__all__"


    
    def create(self, validated_data):
        """✅ Ensure vehicles are assigned to the logged-in user's company"""
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['company'] = user.company  # ✅ Assign vehicle to user's company
        return super().create(validated_data)    


class InventoryStatusSerializer(serializers.ModelSerializer):
    status_name_display = serializers.CharField(source="get_availability_display", read_only=True)  
    
    class Meta:
        model = InventoryStatus
        fields = "__all__"

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"




class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = '__all__'