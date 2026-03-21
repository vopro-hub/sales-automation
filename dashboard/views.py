from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from leads.models import Lead, EscalationEvent
from bookings.models import BookingEvent
from django.utils.timezone import now, timedelta
from .serializers import LeadSerializer

class OverviewMetrics(APIView):
    permission_classes = [IsAuthenticated]
     
    def get(self, request):
        user = request.user
        tenant = user.tenant
        today = now().date()
        
        leads_qs = Lead.objects.filter(tenant=tenant)
        bookings_qs = BookingEvent.objects.filter(tenant=tenant)
        escalations_qs = EscalationEvent.objects.filter(tenant=tenant)

        # Agent sees only their data
        if user.role == "agent":
            leads_qs = leads_qs.filter(assigned_agent=user)
            bookings_qs = bookings_qs.filter(tenant=tenant)
            escalations_qs = escalations_qs.filter(assigned_agent=user)
        
        data = {
            "leads_today": leads_qs.filter(created_at__date=today).count(),
            "qualified_leads": leads_qs.filter(stage="qualified").count(),
            "bookings": bookings_qs.filter(status="booked").count(),
            "escalations": escalations_qs.filter(resolved=False).count(),
        }

        return Response(data)

class LeadsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tenant = user.tenant

        leads = Lead.objects.filter(tenant=tenant)

        if user.role == "agent":
            leads = leads.filter(assigned_agent=user)

        leads = leads.select_related("tenant").order_by("-created_at")

        return Response(LeadSerializer(leads, many=True).data)


class EscalationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tenant = user.tenant

        escalations = EscalationEvent.objects.filter(
            tenant=tenant,
            resolved=False
        ).select_related("lead", "tenant")

        if user.role == "agent":
            escalations = escalations.filter(assigned_agent=user)

        data = [{
            "tenant": e.tenant.name,
            "phone": e.lead.phone,
            "reason": e.reason,
            "created_at": e.created_at,
        } for e in escalations]

        return Response(data)


class ResolveEscalation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, escalation_id):
        user = request.user

        escalation = EscalationEvent.objects.get(
            id=escalation_id,
            tenant=user.tenant
        )

        # Optional: agents can only resolve their own
        if user.role == "agent" and escalation.assigned_agent != user:
            return Response({"error": "Forbidden"}, status=403)

        escalation.resolved = True
        escalation.save()

        return Response({"status": "resolved"})


