import requests
from django.conf import settings

WHATSAPP_TOKEN = "https://graph.facebook.com/v19.0/messages"

from core.branding import get_branding

def send_whatsapp_message(tenant, phone, message):
    branding = get_branding(tenant)

    payload = {
        "to": phone,
        "sender_name": branding["whatsapp_sender"],
        "message": message,
    }
    requests.post(
        settings.WHATSAPP_API_URL,
        headers={
            "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"
        },
        json= payload
    )
