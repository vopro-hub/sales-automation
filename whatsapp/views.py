import json
import hmac
import hashlib
from urllib import request
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

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
        token = request.data.get("token")
        
        existing = WhatsAppSession.objects.filter(user=user).first()

        # If session exists and user didn't confirm relink
        if existing and not request.data.get("force"):
            return Response({
                "has_session": True,
                "message": "You already have a WhatsApp session. Relink?",
            }, status=200)

        

        session_id = str(uuid.uuid4())

        create_session(session_id, token)
        print("Session id:", session_id)
        return Response({
            "session_id": session_id,
            "has_session": False
        })

class WhatsAppConnectedView(APIView):
    permission_classes = [IsAuthenticated]  # or remove if internal

    def post(self, request):
        session_id = request.data.get("session_id")
        user = request.user
        print("user is:", request.user)
        
        # Delete old session if relinking
        existing = WhatsAppSession.objects.filter(user=user).first()
        if existing:
            existing.delete()
            
        WhatsAppSession.objects.create(
            tenant=user.tenant,
            user=user,
            session_id=session_id,
            status="connected"
        )

        return Response({"status": "saved"})

class QRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        session_id = request.query_params.get("session")
    
        if not session_id:
            return Response({"error": "No session_id"}, status=400)
    
        qr = get_qr_code(session_id)
    
        return Response({
            "qr": qr.get("qr"),
            "connected": qr.get("connected", False)
        })

@csrf_exempt
@ratelimit(key="ip", rate="30/m", block=True)
def whatsapp_webhook(request):

    if request.method == "POST":

        try:
            payload = json.loads(request.body)

            # ✅ NEW FORMAT (from Node WPPConnect)
            session_id = payload.get("session")
            from_number = payload.get("from")
            text = payload.get("body")

            if not session_id or not from_number or not text:
                print("⚠️ Invalid payload:", payload)
                return JsonResponse({"status": "ignored_invalid"}, status=200)
        except Exception:
            return JsonResponse({"status": "invalid_payload"}, status=400)

        # 🔥 GET SESSION (THIS WAS MISSING)
        
        session = WhatsAppSession.objects.filter(
            session_id=session_id
        ).first()
        
        # 🔥 AUTO-RECOVER (CRITICAL FIX)
        if not session:
            print("⚠️ Session not found, auto-creating:", session_id)
        
            # ⚠️ You don't have user context here → create minimal session
            session = WhatsAppSession.objects.create(
                session_id=session_id,
                status="connected"
            )

        tenant = session.tenant

        # CREATE OR GET LEAD
        if not from_number:
            return JsonResponse({"status": "no_sender"}, status=200)

        lead, _ = Lead.objects.get_or_create(
            tenant=tenant,
            phone=from_number
        )

        # SAVE MESSAGE
        Message.objects.create(
            tenant=tenant,
            lead=lead,
            sender="lead",
            content=text
        )

        # PROCESS AI
        handle_incoming_message(
            tenant=tenant,
            lead=lead,
            message=text,
            session=session,
            agent=None  # you can improve later
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