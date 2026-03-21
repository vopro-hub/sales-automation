from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DailyMetrics, SLAViolation
from analytics.serializers import (
    DailyMetricsSerializer,
    SLAViolationSerializer
)
from analytics.services.summary import get_summary
from analytics.services.agents import get_agent_performance


class AnalyticsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_summary(request.user.tenant)
        return Response(data)

class FunnelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        metrics = DailyMetrics.objects.filter(
            tenant=request.user.tenant
        )

        received = sum(m.leads_received for m in metrics)
        qualified = sum(m.leads_qualified for m in metrics)
        booked = sum(m.leads_booked for m in metrics)

        return Response({
            "received": received,
            "qualified": qualified,
            "booked": booked,
            "conversion_rate": round(
                (booked / received) * 100, 2
            ) if received else 0,
        })

class AgentAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_agent_performance(request.user.tenant)
        return Response(data)

class SLAAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        violations = SLAViolation.objects.filter(
            tenant=request.user.tenant
        ).order_by("-created_at")

        serializer = SLAViolationSerializer(violations, many=True)
        return Response(serializer.data)


class AIImpactView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        metrics = DailyMetrics.objects.filter(
            tenant=request.user.tenant
        )

        ai_only = sum(m.ai_only_conversions for m in metrics)
        human = sum(m.human_assisted_conversions for m in metrics)

        total = ai_only + human

        return Response({
            "ai_only": ai_only,
            "human_assisted": human,
            "ai_percentage": round(
                (ai_only / total) * 100, 2
            ) if total else 0,
        })

