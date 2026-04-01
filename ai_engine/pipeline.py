from leads.models import Message, FollowUpState
from ai_engine.responder import generate_ai_reply
from ai_engine.qualification import update_qualification
from whatsapp.sender import send_whatsapp_message
from ai_engine.escalation import check_escalation
from notifications.agent import notify_agent


MAX_AI_MESSAGES = 50


def handle_incoming_message(tenant, lead, message, session, agent):
    """
    Main AI pipeline for processing incoming WhatsApp messages.
    Supports multi-tenant and multi-agent WhatsApp sessions.
    """

    # Stop follow-up automation when the lead replies
    FollowUpState.objects.filter(lead=lead).update(completed=True)

    # Limit AI messages per lead to prevent loops or abuse
    ai_message_count = Message.objects.filter(
        lead=lead,
        sender="ai"
    ).count()

    if ai_message_count >= MAX_AI_MESSAGES:
        notify_agent(tenant, lead, "ai_limit_reached")
        return

    # Check if escalation is required
    escalate, reason = check_escalation(
        tenant,
        lead,
        message
    )

    if escalate:
        notify_agent(tenant, lead, reason)

        send_whatsapp_message(
            session_id=session.session_id,
            to=lead.phone,
            text="Thanks for sharing this. I’m notifying an agent so they can personally assist you."
        )

        return  # AI stops here

    # Generate AI response
    ai_response = generate_ai_reply(
        tenant,
        lead,
        message
    )

    # Save AI message to database
    Message.objects.create(
        tenant=tenant,
        lead=lead,
        sender="ai",
        content=ai_response
    )

    # Update qualification signals
    update_qualification(
        lead,
        message
    )
    
    print("🤖 AI RESPONSE:", ai_response)
    print("📤 SENDING TO:", lead.phone)
    print("📤 SESSION:", session.session_id)
    # Send WhatsApp reply using the correct agent session
    send_whatsapp_message(
        session_id=session.session_id,
        to=lead.phone,
        text=ai_response
    )