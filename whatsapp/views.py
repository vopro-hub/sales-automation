import json
import hmac
import hashlib
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit

from .models import WhatsAppSession
from leads.models import Lead, Message
from ai_engine.pipeline import handle_incoming_message

from .services import create_session, get_qr_code


class StartWhatsAppSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        existing = WhatsAppSession.objects.filter(user=user).first()

        # If session exists and user didn't confirm relink
        if existing and not request.data.get("force"):
            return Response({
                "has_session": True,
                "message": "You already have a WhatsApp session. Relink?",
            }, status=200)

        # Delete old session if relinking
        if existing:
            existing.delete()

        session_id = str(uuid.uuid4())

        WhatsAppSession.objects.create(
            tenant=user.tenant,
            user=user,
            session_id=session_id,
            status="connecting"
        )

        create_session(session_id)

        return Response({
            "session_id": session_id,
            "has_session": False
        })


class QRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            session = WhatsAppSession.objects.get(user=request.user)
        except WhatsAppSession.DoesNotExist:
            return Response({"error": "No session"}, status=404)

        qr = get_qr_code(session.session_id)
       
        return Response({
            "qr": qr.get("qr"),
            "status": session.status
        })

@csrf_exempt
@ratelimit(key="ip", rate="60/m", block=True)
def whatsapp_webhook(request):
    """
    Receives incoming WhatsApp messages from the WPPConnect gateway.
    Routes the message to the correct tenant, lead, and AI pipeline.
    """

    if request.method != "POST":
        return JsonResponse({"status": "method_not_allowed"}, status=405)

    if not verify_signature(request):
        return HttpResponseForbidden("Invalid webhook signature")

    try:
        payload = json.loads(request.body)

        session_id = payload.get("session")
        from_number = payload.get("from")
        text = payload.get("body")
        is_group = payload.get("isGroupMsg", False)

    except Exception:
        return JsonResponse({"status": "invalid_payload"}, status=400)

    # Ignore group messages
    if is_group:
        return JsonResponse({"status": "ignored_group"})

    # Find the WhatsApp session
    try:
        session = WhatsAppSession.objects.select_related("tenant", "user").get(
            session_id=session_id,
            status="connected"
        )
    except WhatsAppSession.DoesNotExist:
        return JsonResponse({"status": "unknown_session"}, status=404)

    tenant = session.tenant
    agent = session.user

    # Normalize number
    from_number = from_number.replace("@c.us", "")

    # Get or create lead
    lead, _ = Lead.objects.get_or_create(
        tenant=tenant,
        phone=from_number
    )

    # Save incoming message
    Message.objects.create(
        tenant=tenant,
        lead=lead,
        sender="lead",
        content=text,
        metadata={
            "session_id": session_id,
            "agent_id": agent.id
        }
    )

    # Send to AI engine
    handle_incoming_message(
        tenant=tenant,
        lead=lead,
        message=text,
        session=session,
        agent=agent
    )

    return JsonResponse({"status": "ok"})

def verify_signature(request):
    """
    Verify webhook authenticity from the WPPConnect gateway.
    """

    signature = request.headers.get("X-WPP-Signature")
    if not signature:
        return False

    body = request.body

    expected = hmac.new(
        settings.WPP_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)