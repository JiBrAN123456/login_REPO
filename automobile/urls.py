# project_name/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include the user-related URLs
    path('api/', include('login.urls')),  # This maps /api/ to your login app URLs
]
