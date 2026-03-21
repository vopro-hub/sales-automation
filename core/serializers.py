from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Tenant

User = get_user_model()

class TenantSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "staff_ID",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        tenant = self.context["tenant"]

        user = User.objects.create_user(
            staff_ID=validated_data["staff_ID"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            whatsapp_number=validated_data.get("whatsapp_number"),
            password=validated_data["password"],
            tenant=tenant,
            role=validated_data["role"],
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source="tenant.name")

    class Meta:
        model = User
        fields = ["id", "email", "tenant_name", "role"]
