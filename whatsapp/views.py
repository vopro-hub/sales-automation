from django.shortcuts import render
import hmac
import hashlib
from django.conf import settings
import json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from core.models import Tenant
from leads.models import Lead, Message
from ai_engine.pipeline import handle_incoming_message
from django_ratelimit.decorators import ratelimit

@ratelimit(key="ip", rate="30/m", block=True) # Protect agains spam attacks, costly AI abuse and accidental loops
@csrf_exempt
def whatsapp_webhook(request):
    payload = json.loads(request.body)

    from_number = payload["from"]
    to_number = payload["to"]
    text = payload["message"]["text"]

    tenant = Tenant.objects.get(
        whatsapp_number=to_number,
        is_active=True
    )

    lead, _ = Lead.objects.get_or_create(
        tenant=tenant,
        phone=from_number
    )

    Message.objects.create(
        tenant=tenant,
        lead=lead,
        sender="lead",
        content=text
    )

    handle_incoming_message(tenant, lead, text)

    return JsonResponse({"status": "ok"})


def verify_signature(request):
    signature = request.headers.get("X-Hub-Signature-256")
    body = request.body

    expected = hmac.new(
        settings.WHATSAPP_TOKEN.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    return signature == f"sha256={expected}"
