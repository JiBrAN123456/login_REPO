from django.shortcuts import render
from rest_framework import viewsets
from .models import Document, Vehicle , InventoryStatus
from .serializers import DocumentSerializer,VehicleSerializer, InventoryStatusSerializer
from rest_framework.permissions import IsAuthenticated ,  IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class DocumentViewSet(viewsets.ModelViewSet):
  
    serializer_class = DocumentSerializer
    authentication_classes = [IsAuthenticated]

    def get_queryset(self):
        
        queryset = Document.objects.select_related('vehicle')
        vehicle_id = self.request.query_params.get('vehicle')
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        return queryset    
    

class InventoryViewSet(viewsets.ModelViewSet):

    serializer_class = InventoryStatusSerializer
    queryset =  InventoryStatus.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class VehiclePagination(PageNumberPagination):
    page_size = 10  # Number of vehicles per page
    page_size_query_param = 'page_size'  # Allow changing page size in URL
    max_page_size = 100  # Prevent loading too many records at once




class VehicleViewSet(viewsets.ModelViewSet):
     
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    pagination_class = VehiclePagination    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['price','year']
    ordering = ['-year']



    def get_queryset(self):
        queryset = Vehicle.objects.all()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def perform_update(self, serializer):
        
        instance = serializer.save()


        if not Vehicle.objects.filter(status="available").exists():
            Inventory_status, _ = Inventory_status.objects.get_or_create(status='sold_out')
        else:
            inventory_status, _ = InventoryStatus.objects.get_or_create(status="available")

        inventory_status.save()    