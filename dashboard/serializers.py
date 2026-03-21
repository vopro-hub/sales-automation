from rest_framework import serializers
from leads.models import Lead

class LeadSerializer(serializers.ModelSerializer):
    tenant = serializers.CharField(source="tenant.name")

    class Meta:
        model = Lead
        fields = ("tenant", "phone", "stage", "score", "created_at")
