from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv 

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = [os.getenv("Frontend_URL")]  # Allow all domains (change this in production)

# ✅ Multi-Tenant Configuration
SHARED_APPS = [
    "django_tenants",  # Must be the first app
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "rest_framework",
    "rest_framework_simplejwt",
    "simple_history",
    "login",  # Shared authentication app
]

TENANT_APPS = [
   
    "inventory",  # Inventory models (tenant-specific)
   
]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "automobile.urls"
PUBLIC_SCHEMA_URLCONF = "automobile.public_urls"  # ✅ Make sure this file exists

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "automobile.wsgi.application"

# ✅ Multi-Tenant PostgreSQL Configuration
DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",  # Multi-Tenant PostgreSQL Backend
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("USERNAME"),
        "PASSWORD": os.getenv("PASSWORD"),
        "HOST": os.getenv("HOST"),
        "PORT": os.getenv("PORT"),
        "OPTIONS": {
            "options": "-c search_path=public"  # Default schema
        },
    }
}

DATABASE_ROUTERS = ["django_tenants.routers.TenantSyncRouter"]  # ✅ Ensure it's enabled

AUTH_USER_MODEL = "login.User"

# ✅ JWT Authentication
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,  # Show 10 vehicles per page
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

TENANT_MODEL = "login.Company"  # ✅ Tenant model
TENANT_DOMAIN_MODEL = "login.Domain"

# ✅ Static & Media Files
STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ✅ Time & Localization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
