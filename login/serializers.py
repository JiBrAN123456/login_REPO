from rest_framework import serializers
from .models import User, Profile, Company, Role


class UserSerializer(serializers.ModelSerializer):
      class Meta:
            model = User
            fields = ['email','password','company']
            extra_kwargs = {'password': {'write_only':True}}

            def create(self, validated_data):
                  password = validated_data.pop('password')
                  user = User.objects.create(**validated_data)
                  user.set_password(password)
                  user.save()
                  return user
            

class ProfileSerializer(serializers.ModelSerializer):
      class Meta:
            model = Profile
            fields = "__all__"          