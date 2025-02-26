#!/bin/bash
set -e  # Exit on error

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations for shared apps..."
python manage.py migrate_schemas --shared

echo "Initializing public tenant..."
RENDER_EXTERNAL_HOSTNAME="${RENDER_EXTERNAL_HOSTNAME:-localhost}" python manage.py init_public_tenant

echo "Running migrations for all schemas..."
python manage.py migrate_schemas

echo "Creating superuser..."
python manage.py shell << END
from login.models import Company, Domain, User
try:
    company = Company.objects.get(schema_name='public')
    if not User.objects.filter(email='admin@example.com').exists():
        User.objects.create_superuser(
            email='admin@example.com',
            password='Admin@123',
            company=company,
            username='admin'
        )
        print("Superuser created successfully")
except Exception as e:
    print(f"Error creating superuser: {str(e)}")
END 