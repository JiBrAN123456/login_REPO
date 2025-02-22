from rest_framework import serializers
from .models import User, Company, Role, Menu, RoleMenuPermissions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_guid', 'username', 'email', 'mobile_number', 'is_active', 'company', 'role', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            password = validated_data.pop("password", None)  # Extract password separately
            company = validated_data.pop("company", None)  # Extract company separately
            role = validated_data.pop("role", None)  # Extract role separately
        
            user = User.objects.create(**validated_data)  # Create user
            if password:
               user.set_password(password)  # Set hashed password
               user.company = company  # Assign company
               user.role = role  # Assign role
               user.save()
        
            return user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class RoleMenuPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMenuPermissions
        fields = '__all__'

