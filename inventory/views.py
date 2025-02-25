from rest_framework import viewsets, permissions
from .models import Vehicle, InventoryStatus, Document, VehicleImage
from .serializers import VehicleSerializer, InventoryStatusSerializer, DocumentSerializer, VehicleImageSerializer
from login.models import Company
from rest_framework.response import Response

class VehicleViewSet(viewsets.ModelViewSet):
    """
    ✅ Vehicle API (Multi-Tenant)
    - Users can only access vehicles from their company
    - Admins can manage all vehicles
    """
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """✅ Filter vehicles by company"""
        user = self.request.user
        return Vehicle.objects.filter(company=user.company, is_deleted=False)

    def perform_create(self, serializer):
        """✅ Auto-assign vehicle to logged-in user's company"""
        serializer.save(created_by=self.request.user, company=self.request.user.company)

class InventoryStatusViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryStatusSerializer
    queryset = InventoryStatus.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """✅ Filter documents by company"""
        user = self.request.user
        return Document.objects.filter(vehicle__company=user.company)

class VehicleImageViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """✅ Filter images by company"""
        user = self.request.user
        return VehicleImage.objects.filter(vehicle__company=user.company)
