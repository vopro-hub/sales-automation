from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Plan, Invoice


class PaymentWebhook(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        reference = data.get("reference")
        status = data.get("status")

        if not reference:
            return Response({"error": "Missing reference"}, status=400)

        try:
            invoice = Invoice.objects.get(reference=reference)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=404)

        if status == "success":
            invoice.mark_paid()

        return Response({"status": "ok"})

class PlanList(APIView):
    permission_classes = []

    def get(self, request):
        plans = Plan.objects.all()
        return Response([
            {
                "id": plan.id,
                "name": plan.name,
                "price": str(plan.price_monthly),
                "discount": str(plan.price_discount),
                "max_agents": plan.max_agents,
                "max_leads": plan.max_leads_per_month,
                "features": [
                    f.strip()
                    for f in plan.features.split(",")
                    if f.strip()
                ],
            }
            for plan in plans
        ])
