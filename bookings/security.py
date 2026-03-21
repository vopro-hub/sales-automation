import hmac
import hashlib
from django.conf import settings

def verify_booking_signature(request):
    signature = request.headers.get("X-Webhook-Signature")
    if not signature:
        return False

    expected = hmac.new(
        settings.BOOKING_WEBHOOK_SECRET.encode(),
        request.body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)
