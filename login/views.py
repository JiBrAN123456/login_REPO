from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, Profile, Company
from .serializers import UserSerializer,ProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        company_name = data.get('company')


        company, _ = Company.objects.get_or_create(name=company_name)

        user = User.objects.create_user(email=email, password=password, company=company)
        Profile.objects.create(user=user, full_name=data.get('full_name'), role=data.get('role'))

        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)


class LoginAPIView(TokenObtainPairView):
    pass



class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)