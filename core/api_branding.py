from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def branding(request):
    tenant = request.user.tenant

    return Response({
        "name": tenant.display_name(),
        "logo": tenant.logo_url,
        "primary_color": tenant.primary_color,
    })
