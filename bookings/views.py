import json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from whatsapp.sender import send_whatsapp_message
from leads.models import Lead, FollowUpState
from bookings.models import BookingEvent
from bookings.security import verify_booking_signature
from notifications.agent import notify_agent
from core.audit import log_action

@csrf_exempt
def booking_webhook(request):
    if request.method != "POST":
        return JsonResponse({"status": "invalid"}, status=400)

    if not verify_booking_signature(request):
        return HttpResponseForbidden("Invalid signature")

    payload = json.loads(request.body)

    # Normalize fields (adjust to your booking provider)
    phone = payload.get("phone")
    email = payload.get("email")
    booking_time = payload.get("start_time")

    lead = (
        Lead.objects.filter(phone=phone).first()
        or Lead.objects.filter(email=email).first()
    )

    if not lead:
        return JsonResponse({"status": "lead_not_found"}, status=404)

    BookingEvent.objects.update_or_create(
        lead=lead,
        defaults={
            "tenant": lead.tenant,
            "status": "booked",
            "scheduled_at": booking_time,
        }
    )

    # Stop follow-ups immediately
    FollowUpState.objects.filter(lead=lead).update(completed=True)

    # Update lead stage
    lead.stage = "booked"
    lead.save(update_fields=["stage"])

    # Notify agent
    notify_agent(
        lead.tenant,
        lead,
        reason="booking_confirmed"
    )
    
    send_whatsapp_message(
        tenant=lead.tenant,
        phone=lead.phone,
        message =f"Your appointment is confirmed. {lead.tenant.display_name()} will speak with you at the scheduled time."
    )

    if payload.get("event") == "booking.cancelled":
        BookingEvent.objects.filter(lead=lead).update(status="cancelled")
        lead.stage = "qualified"
        lead.save()

    log_action(
        tenant=lead.tenant,
        user=None,
        action="booking_confirmed",
        object_type="booking",
        object_id=lead.id,
        message="Booking confirmed via webhook",
    )

    return JsonResponse({"status": "confirmed"})

