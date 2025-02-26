#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate_schemas --shared
python manage.py init_public_tenant
python manage.py migrate_schemas 