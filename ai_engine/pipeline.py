from leads.models import Message, FollowUpState
from ai_engine.responder import generate_ai_reply
from ai_engine.qualification import update_qualification
from whatsapp.sender import send_whatsapp_message
from ai_engine.escalation import check_escalation
from notifications.agent import notify_agent

def handle_incoming_message(tenant, lead, user_message):
     # stop follow-ups on reply
    FollowUpState.objects.filter(lead=lead ).update(completed=True)
    
    # limit messages per lead
    MAX_AI_MESSAGES = 20
    
    if Message.objects.filter(lead=lead, sender="ai").count() > MAX_AI_MESSAGES:
        notify_agent(tenant, lead, "ai_limit_reached")
        return
    
    escalate, reason = check_escalation( tenant, lead, user_message)

    if escalate:
        notify_agent(tenant, lead, reason)

        send_whatsapp_message(
            lead.phone,
            "Thanks for sharing this. I’m notifying my Boss so he can personally assist you."
        )
        return  # AI steps back
    
    ai_response = generate_ai_reply(tenant, lead, user_message)

    Message.objects.create(
        tenant=tenant,
        lead=lead,
        sender="ai",
        content=ai_response
    )

    update_qualification(lead, user_message)

    send_whatsapp_message(
        to=lead.phone,
        text=ai_response
    )

CELERY_BEAT_SCHEDULE = {
    "run-followups-every-hour": {
        "task": "leads.tasks.run_followups",
        "schedule": 3600,
    }
}
