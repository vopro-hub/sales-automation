from rest_framework import serializers
from analytics.models import DailyMetrics, SLAViolation


class DailyMetricsSerializer(serializers.ModelSerializer):
    conversion_rate = serializers.SerializerMethodField()

    class Meta:
        model = DailyMetrics
        fields = "__all__"

    def get_conversion_rate(self, obj):
        if obj.leads_received == 0:
            return 0
        return round(
            (obj.leads_booked / obj.leads_received) * 100, 2
        )


class SLAViolationSerializer(serializers.ModelSerializer):
    lead_id = serializers.IntegerField(source="lead.id")
    agent_email = serializers.CharField(
        source="agent.email",
        allow_null=True
    )

    class Meta:
        model = SLAViolation
        fields = [
            "id",
            "lead_id",
            "agent_email",
            "violation_type",
            "seconds_late",
            "created_at",
        ]
