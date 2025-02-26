from django.core.management.base import BaseCommand
from login.models import Company, Domain
import os

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
            
            # Get the hostname from environment or use default
            hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME', 'localhost')
            
            # Create domains for both localhost and render.com
            domains = ['localhost', hostname]
            for domain_name in domains:
                domain, domain_created = Domain.objects.get_or_create(
                    domain=domain_name,
                    defaults={
                        'tenant': company,
                        'is_primary': domain_name == hostname
                    }
                )
                if domain_created:
                    self.stdout.write(self.style.SUCCESS(f'Created domain: {domain.domain}'))
            
            self.stdout.write(self.style.SUCCESS('Public tenant initialization complete!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 