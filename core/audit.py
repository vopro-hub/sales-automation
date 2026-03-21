from core.models import AuditLog

def log_action(
    *,
    tenant,
    action,
    object_type,
    object_id,
    user=None,
    message="",
    metadata=None,
    ip=None,
):
    AuditLog.objects.create(
        tenant=tenant,
        user=user,
        action=action,
        object_type=object_type,
        object_id=str(object_id),
        message=message,
        metadata=metadata or {},
        ip_address=ip,
    )
