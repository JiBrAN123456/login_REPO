from rest_framework import generics, permissions
from .models import User, Company , Role ,Menu ,RoleMenuPermissions
from .serializers import UserSerializer ,CompanySerializer , RoleMenuPermissionsSerializer ,RoleSerializer ,MenuSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django_tenants.utils import get_tenant

class HasPermission(BasePermission):
    """
    Custom permission class to check if the user has the required permission.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated  or not hasattr(request.user, "profile"):
            return False

        profile = request.user.profile  # Ensure user has a profile
        required_permission = getattr(view, "required_permission", None)

        if required_permission:
            module, action = required_permission.split(".")
            return profile.has_permission(module, action)
        return True


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        print("Received Data:", request.data)  # Debugging
        return super().create(request, *args, **kwargs)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.profile.role.name if self.user.profile and self.user.profile.role else None
        data['company'] = self.user.company.name if self.user.company else None
        return data

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)    
    

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "company.view"


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "company.manage"  

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "role.view"

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "role.manage"

class MenuListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "menu.view"

class RoleMenuPermissionsListCreateView(generics.ListCreateAPIView):
    queryset = RoleMenuPermissions.objects.all()
    serializer_class = RoleMenuPermissionsSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permission = "permissions.manage"

def debug_view(request):
    return JsonResponse({
        'message': 'Debug endpoint working',
        'path': request.path,
        'method': request.method
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    tenant = get_tenant(request)
    return Response({
        'status': 'healthy',
        'tenant': tenant.schema_name,
        'domain': request.get_host()
    })