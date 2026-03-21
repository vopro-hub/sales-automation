from whatsapp.sender import send_whatsapp_message

def notify_agent(tenant, lead, reason):
    message = (
        f"ESCALATION ALERT\n\n"
        f"Tenant: {tenant.name}\n"
        f"Lead: {lead.phone}\n"
        f"Reason: {reason}\n"
        f"Stage: {lead.stage}\n"
        f"Score: {lead.score}"
    )
    
    agent = lead.assigned_agent
    if not agent:
        send_whatsapp_message(to="ADMIN_PHONE_NUMBER", text=message)
        return
    
    # Option 1: WhatsApp to agent
    send_whatsapp_message(
        to="AGENT_PHONE_NUMBER",
        user=agent,
        message=f"Lead {lead.name}: {reason}"
    )
    
    

    # Option 2 (later): Email / Slack
    
    # Human mode flag on Lead
    lead.is_human_handled = True
    lead.save()
