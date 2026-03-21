from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from .models import Lead
from ai_engine.qualification import start_ai_qualification
from .api_assignment import assign_agent
from core.audit import log_action

User = get_user_model()


class ManualLeadCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        agents = User.objects.filter(
            tenant=request.user.tenant,
            role="agent"
        ).values("id", "staff_ID", "email")

        return Response(agents)

    def post(self, request):

        data = request.data
        user = request.user
        tenant = request.user.tenant

        assigned_agent = None

        # Manager manually assigns agent
        if data.get("assigned_agent_id"):
            assigned_agent = User.objects.filter(
                id=data["assigned_agent_id"],
                tenant=tenant,
                role="agent"
            ).first()

        # Auto assign if creator is agent
        elif user.role == "agent":
            assigned_agent = user

        lead = Lead.objects.create(
            tenant=tenant,
            name=data.get("name"),
            phone=data.get("phone"),
            email=data.get("email", ""),
            source="manual",
            stage=data.get("stage"),
            notes=data.get("notes", ""),
            assigned_agent=assigned_agent
        )

        # Optional: start AI immediately
        if data.get("start_ai") is True:
            start_ai_qualification.delay(lead.id)

        log_action(
            tenant=tenant,
            user=user,
            action="lead_created",
            object_type="lead",
            object_id=lead.id,
            message="Lead created manually",
        )

        return Response(
            {"id": lead.id, "status": "created"},
            status=status.HTTP_201_CREATED
        )