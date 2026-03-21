from rest_framework import serializers
from .models import Tenant
from core.utils.slug import generate_unique_tenant_slug

class TenantOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            "name",
            "brand_name",
            "logo_url",
            "primary_color",
            "whatsapp_number",
            "whatsapp_sender_name",
            "system_prompt",
        ]

    def validate_whatsapp_number(self, value):
        if Tenant.objects.filter(whatsapp_number=value).exists():
            raise serializers.ValidationError(
                "This WhatsApp number is already in use."
            )
        return value

    def create(self, validated_data):
        tenant_brand_name = validated_data["brand_name"]
        tenant = Tenant.objects.create(
            **validated_data,
            slug=generate_unique_tenant_slug(tenant_brand_name),
            is_active=True
        )
        return tenant