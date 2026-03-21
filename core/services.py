from .models import Tenant

def get_tenant_by_whatsapp_number(number: str) -> Tenant:
    return Tenant.objects.get(
        whatsapp_number=number,
        is_active=True
    )
