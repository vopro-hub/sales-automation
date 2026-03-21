from django.core.management.base import BaseCommand
from core.models import User, Tenant

class Command(BaseCommand):
    help = "Create a superuser with tenant"

    def handle(self, *args, **options):
        email = input("Email: ")
        password = input("Password: ")
        tenant_name = input("Tenant name: ")

        tenant, _ = Tenant.objects.get_or_create(
            name=tenant_name,
        )

        user = User.objects.create_superuser(
            email=email,
            password=password,
            tenant=tenant
        )

        self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
