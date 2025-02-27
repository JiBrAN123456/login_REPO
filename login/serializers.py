from rest_framework import serializers
from .models import User, Company, Role, Menu, RoleMenuPermissions

''' def create(self, validated_data):
        password = validated_data.pop("password", None)  # Extract password
        user = User.objects.create(**validated_data)  # Create user
        if password:
            user.set_password(password)  # Hash password
        user.save()
        return user'''

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_guid', 'username', 'email', 'password', 'mobile_number', 'is_active', 'company', 'created_at']  # ❌ Removed role
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        company_id = validated_data.pop("company", None)

        company = None

        # Validate company
        if isinstance(company_id, int):  # Ensure it's an integer
           try:
              company = Company.objects.get(id=company_id)
           except Company.DoesNotExist:
                raise serializers.ValidationError({"company": "Invalid company ID."}) 
        else:
           company = company_id

        # Create the user
        user = User.objects.create(company=company, **validated_data)

        if password:
            user.set_password(password)  # Hash password
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

