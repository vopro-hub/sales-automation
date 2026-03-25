import requests

WPP_URL = "http://localhost:3001/messages/send"


def send_whatsapp_message(session_id, to, text):
    try:
        # 🔥 Normalize phone (VERY IMPORTANT)
        to = str(to).replace("+", "").strip()

        payload = {
            "session": session_id,
            "to": to,
            "message": text
        }

        print("📤 SENDING:", payload)

        res = requests.post(WPP_URL, json=payload, timeout=5)

        print("📥 RESPONSE:", res.status_code, res.text)

    except Exception as e:
        print("❌ SEND ERROR:", str(e))