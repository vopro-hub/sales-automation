from django.utils import timezone
from datetime import timedelta
from leads.models import FollowUpState, FollowUpConfig
from bookings.models import BookingEvent
from leads.followup_messages import (
    step_1_message,
    step_2_message,
    step_3_message
)
from whatsapp.sender import send_whatsapp_message

def process_lead_followup(lead):
    tenant = lead.tenant

    config = FollowUpConfig.objects.filter(
        tenant=tenant,
        is_active=True
    ).first()

    if not config:
        return

    state, _ = FollowUpState.objects.get_or_create(lead=lead)

    if state.completed:
        return

    # Stop if booked
    if BookingEvent.objects.filter(
        lead=lead,
        status="booked"
    ).exists():
        state.completed = True
        state.save()
        return

    now = timezone.now()
    created = lead.created_at
    
    if not state.step_1_sent:
        if created + timedelta(hours=config.step_1_delay) <= now:
            send_step_1(lead)
            state.step_1_sent = True

    elif not state.step_2_sent:
        if created + timedelta(hours=config.step_2_delay) <= now:
            send_step_2(lead)
            state.step_2_sent = True

    elif not state.step_3_sent:
        if created + timedelta(hours=config.step_3_delay) <= now:
            send_step_3(lead)
            state.step_3_sent = True
            state.completed = True

    state.save()


def send_step_1(lead):
    send_whatsapp_message(lead.phone, step_1_message())

def send_step_2(lead):
    send_whatsapp_message(lead.phone, step_2_message())

def send_step_3(lead):
    send_whatsapp_message(lead.phone, step_3_message())

