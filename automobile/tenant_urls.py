from django.urls import path, include

urlpatterns = [
    path('api/', include('login.urls')),  # API routes for tenants
]
