from leads.models import Message
import openai

def generate_ai_reply(tenant, lead, user_message):
    history = Message.objects.filter(
        lead=lead
    ).order_by("created_at")[:10]

    messages = [
        {"role": "system", "content": tenant.system_prompt}
    ]

    for msg in history:
        role = "assistant" if msg.sender == "ai" else "user"
        messages.append({"role": role, "content": msg.content})

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message["content"]
