from rest_framework.decorators import api_view, permission_classes
from core.permissions import IsOwner
from rest_framework.response import Response

@api_view(["POST"])
@permission_classes([IsOwner])
def update_branding(request):
    tenant = request.user.tenant
    data = request.data

    tenant.brand_name = data.get("brand_name", tenant.brand_name)
    tenant.logo_url = data.get("logo_url", tenant.logo_url)
    tenant.primary_color = data.get("primary_color", tenant.primary_color)
    tenant.whatsapp_sender_name = data.get(
        "whatsapp_sender_name",
        tenant.whatsapp_sender_name
    )
    tenant.save()

    return Response({"status": "updated"})
