import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sales_automator.bookings.models import BookingEvent


@csrf_exempt
def booking_webhook(request):
    payload = json.loads(request.body)

    lead_phone = payload["invitee"]["phone"]

    booking = BookingEvent.objects.filter(
        lead__phone=lead_phone
    ).last()

    if booking:
        booking.status = "booked"
        booking.save()

    return JsonResponse({"status": "ok"})
