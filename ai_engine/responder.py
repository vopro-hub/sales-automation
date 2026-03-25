from leads.models import Message
from openai import OpenAI
from django.conf import settings
import random

client = OpenAI(api_key=settings.OPENAI_API_KEY)

MAX_HISTORY = 12


def generate_ai_reply(tenant, lead, user_message):
    """
    Generates AI response using conversation history.
    Includes simulation mode for testing WhatsApp flow.
    """

    # ✅ SIMULATION MODE (NO OPENAI CALL)
    if getattr(settings, "AI_SIMULATION_MODE", False):

        simulated_responses = [
            f"Got your message: '{user_message}'. Let me help you with that.",
            f"Thanks for reaching out! Can you tell me more about what you're looking for?",
            f"I understand you said '{user_message}'. What would you like to achieve?",
            f"Great question. Based on what you said, I can guide you further.",
            f"You're on the right track. Let me ask — what’s your main goal right now?"
        ]

        return random.choice(simulated_responses)

    # ---------------- REAL AI BELOW ---------------- #

    history = (
        Message.objects
        .filter(tenant=tenant, lead=lead)
        .order_by("-created_at")[:MAX_HISTORY]
    )

    history = reversed(history)

    messages = [
        {
            "role": "system",
            "content": tenant.system_prompt
        }
    ]

    for msg in history:
        if msg.sender in ["ai", "agent"]:
            role = "assistant"
        else:
            role = "user"

        messages.append({
            "role": role,
            "content": msg.content
        })

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
        reply = "Please I need to speak with my manager about this. Kindly give me a small time to get back to you."

    return reply