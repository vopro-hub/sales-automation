import requests
from django.conf import settings


WPP_URL = settings.WPP_CONNECT_URL


def create_session(session_id, token):
    url = f"{WPP_URL}/sessions/start"
    payload = {"session": session_id, "token": token}
    return requests.post(url, json=payload).json()


def get_qr_code(session_id):
    url = f"{WPP_URL}/sessions/qr/{session_id}"
    return requests.get(url).json()


def send_message(session_id, to, message):
    url = f"{WPP_URL}/messages/send"
    payload = {
        "session": session_id,
        "to": to,
        "message": message,
    }
    return requests.post(url, json=payload).json()