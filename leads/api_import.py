import csv
import io

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from leads.models import Lead
from core.models import User
from leads.services.assignment import auto_assign_agent
from ai_engine.qualification import start_ai_qualification
from core.permissions import IsOwnerOrManager
from core.audit import log_action

@api_view(["POST"])
@permission_classes([IsOwnerOrManager])
def import_csv(request):
    csv_file = request.FILES.get("file")

    if not csv_file:
        return Response({"error": "No file"}, status=400)

    decoded = csv_file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    created = 0

    for row in reader:
        phone = row.get("phone")
        if not phone:
            continue

        # Prevent duplicates per tenant
        if Lead.objects.filter(
            tenant=request.user.tenant,
            phone=phone
        ).exists():
            continue

        agent = None
        agent_email = row.get("agent_email")
        if agent_email:
            agent = User.objects.filter(
                tenant=request.user.tenant,
                email=agent_email,
                is_agent=True
            ).first()

        lead = Lead.objects.create(
            tenant=request.user.tenant,
            name=row.get("name", ""),
            phone=phone,
            email=row.get("email"),
            notes=row.get("notes", ""),
            source="import",
            stage="new",
            assigned_agent=agent,
        )

        if not agent:
            auto_assign_agent(request.user.tenant, lead)

        if row.get("start_ai", "").lower() == "yes":
            lead.ai_status = "running"
            lead.save(update_fields=["ai_status"])
            start_ai_qualification.delay(lead.id)

        created += 1
        
        log_action(
            tenant=request.user.tenant,
            user=request.user,
            action="lead_imported",
            object_type="lead",
            object_id=lead.id,
            message="Lead imported via CSV",
        )


    return Response(
        {"created": created},
        status=status.HTTP_201_CREATED
    )
