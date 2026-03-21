from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .tenant_onboarding_serializers import TenantOnboardingSerializer

class TenantOnboardingView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TenantOnboardingSerializer(data=request.data)

        if serializer.is_valid():
            tenant = serializer.save()
            return Response(
                {
                    "message": "Tenant onboarded successfully",
                    "tenant": {
                        "id": tenant.id,
                        "name": tenant.name,
                        "slug": tenant.slug,
                        "signup_url": f"/signup/{tenant.slug}/",
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
