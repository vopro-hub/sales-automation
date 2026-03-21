from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import AuditLog
from core.permissions import IsOwnerOrManager

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsOwnerOrManager])
def audit_logs(request):
    logs = AuditLog.objects.filter(
        tenant=request.user.tenant
    )[:500]

    return Response([
        {
            "id": log.id,
            "action": log.action,
            "object_type": log.object_type,
            "object_id": log.object_id,
            "user": log.user.username if log.user else "system",
            "message": log.message,
            "created_at": log.created_at,
        }
        for log in logs
    ])
