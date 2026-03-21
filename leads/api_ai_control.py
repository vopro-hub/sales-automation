from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Lead
from ai_engine.qualification import start_ai_qualification
from core.audit import log_action

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_ai(request, lead_id):
    lead = Lead.objects.get(id=lead_id, tenant=request.user.tenant)

    if lead.ai_status == "running":
        return Response({"status": "already_running"})

    lead.ai_status = "running"
    lead.ai_locked = True
    lead.save()

    start_ai_qualification.delay(lead.id)

    return Response({"status": "started"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pause_ai(request, lead_id):
    lead = Lead.objects.get(id=lead_id, tenant=request.user.tenant)

    lead.ai_status = "paused"
    lead.save(update_fields=["ai_status"])
    
    log_action(
        tenant=request.user.tenant,
        user=request.user,
        action="ai_started",
        object_type="lead",
        object_id=lead.id,
    )


    return Response({"status": "paused"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def resume_ai(request, lead_id):
    lead = Lead.objects.get(id=lead_id, tenant=request.user.tenant)

    if lead.ai_status != "paused":
        return Response({"status": "not_paused"})

    lead.ai_status = "running"
    lead.save(update_fields=["ai_status"])

    start_ai_qualification.delay(lead.id)
    
    log_action(
        tenant=request.user.tenant,
        user=request.user,
        action="ai_started",
        object_type="lead",
        object_id=lead.id,
    )


    return Response({"status": "resumed"})
