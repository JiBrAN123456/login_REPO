# Generated by Django 5.1.6 on 2025-02-26 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0013_remove_user_role_alter_company_schema_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="mobile_number",
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
