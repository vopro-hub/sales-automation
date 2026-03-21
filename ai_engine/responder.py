from leads.models import Message
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


MAX_HISTORY = 12


def generate_ai_reply(tenant, lead, user_message):
    """
    Generates AI response using conversation history.
    Designed for WhatsApp AI sales automation.
    """

    # Get latest conversation history (most recent first)
    history = (
        Message.objects
        .filter(tenant=tenant, lead=lead)
        .order_by("-created_at")[:MAX_HISTORY]
    )

    # Reverse to chronological order
    history = reversed(history)

    messages = [
        {
            "role": "system",
            "content": tenant.system_prompt
        }
    ]

    for msg in history:

        if msg.sender == "ai":
            role = "assistant"

        elif msg.sender == "agent":
            role = "assistant"

        else:
            role = "user"

        messages.append({
            "role": role,
            "content": msg.content
        })

    # Add the current user message
    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=250
        )

        reply = response.choices[0].message.content.strip()

    except Exception:
        # Fail-safe message if AI API fails
        reply = "Please I need to speak with my manager about this. Kindly give me a small time to get back to you."

    return reply