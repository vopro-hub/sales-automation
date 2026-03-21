from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Lead
from core.models import User
from core.permissions import IsOwnerOrManager
from core.audit import log_action


@api_view(["POST"])
@permission_classes([IsOwnerOrManager])
def assign_agent(request, lead_id):
    agent_id = request.data.get("agent_id")

    lead = Lead.objects.get(
        id=lead_id,
        tenant=request.user.tenant
    )

    agent = User.objects.get(
        id=agent_id,
        tenant=request.user.tenant,
        is_agent=True
    )

    lead.assigned_agent = agent
    lead.save(update_fields=["assigned_agent"])
    
    log_action(
        tenant=request.user.tenant,
        user=request.user,
        action="agent_assigned",
        object_type="lead",
        object_id=lead.id,
        metadata={"agent_id": agent.id},
    )


    return Response({"status": "assigned"})
