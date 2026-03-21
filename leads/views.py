from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import Lead
from .serializers import LeadSerializer

User = get_user_model()

@api_view(["GET"])
def leads_for_user(user,request):
    if user.role in ["owner", "manager"]:
        leads = Lead.objects.filter(tenant=user.tenant).order_by("-last_interaction")

    if user.role =="agent":
        leads = Lead.objects.filter(tenant=user.tenant, assigned_agent=user)

    else: leads = Lead.objects.none()
    
    serializer = LeadSerializer(leads, many=True)
    return Response(serializer.data)





class AgentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        agents = User.objects.filter(
            tenant=request.user.tenant,
            role="agent"
        ).values("id", "staff_ID", "email")

        return Response(agents)