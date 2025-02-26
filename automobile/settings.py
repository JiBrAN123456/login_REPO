from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

ALLOWED_HOSTS = ['*']  # For development
if not DEBUG:
    ALLOWED_HOSTS = [
        'localhost',
        '.render.com',
        os.getenv('RENDER_EXTERNAL_HOSTNAME', ''),
        os.getenv('Frontend_URL', ''),
    ]

DEBUG = True

SHARED_APPS = [
    "django_tenants",
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
    "login",
]

TENANT_APPS = ["inventory"]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # Make sure this is first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'automobile.urls'  # Make sure this points to the correct urls.py
PUBLIC_SCHEMA_URLCONF = 'automobile.public_urls'

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

DATABASES = {
    "default": {
        **dj_database_url.config(default=os.getenv("DATABASE_URL")),
        "ENGINE": "django_tenants.postgresql_backend",
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

SECRET_KEY = os.getenv("SECRET_KEY")  # ✅ Use a secure environment variable

AUTH_USER_MODEL = "login.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

TENANT_MODEL = "login.Company"
TENANT_DOMAIN_MODEL = "login.Domain"

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"