from django.core.management.base import BaseCommand
from login.models import Company, Domain

class Command(BaseCommand):
    help = 'Initialize the public tenant and domain'

    def handle(self, *args, **options):
        try:
            # Create the public schema tenant
            company, created = Company.objects.get_or_create(
                schema_name='public',
                defaults={
                    'name': 'Public Tenant',
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created public tenant: {company.name}'))
            
            # Create a domain for the tenant
            domain, domain_created = Domain.objects.get_or_create(
                domain='localhost',  # Change this to your actual domain in production
                defaults={
                    'tenant': company,
                    'is_primary': True
                }
            )
            
            if domain_created:
                self.stdout.write(self.style.SUCCESS(f'Created domain: {domain.domain}'))
            
            self.stdout.write(self.style.SUCCESS('Public tenant initialization complete!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 