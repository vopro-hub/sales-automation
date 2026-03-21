from bookings.models import BookingConfig, BookingEvent
from whatsapp.sender import send_whatsapp_message

def try_send_booking_link(lead):
    tenant = lead.tenant

    config = BookingConfig.objects.filter(
        tenant=tenant
    ).first()

    if not config:
        return

    if lead.score < config.min_score_required:
        return

    already_sent = BookingEvent.objects.filter(
        lead=lead,
        status="link_sent"
    ).exists()

    if already_sent:
        return

    message = (
        "Thanks for sharing those details. "
        f"{booking_message}"
        f"{config.booking_url}"
    )

    send_whatsapp_message(
        to=lead.phone,
        text=message
    )

    BookingEvent.objects.create(
        tenant=tenant,
        lead=lead,
        status="link_sent"
    )

def booking_message():
    return (
        "I believe a short conversation will help clarify the best options for you. "
        "You can book a convenient time using the link below.\n\n"
    )
