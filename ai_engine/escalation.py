from leads.models import EscalationEvent

ESCALATION_KEYWORDS = {
    "medical": [
        "medical", "health condition", "illness", "diagnosis"
    ],
    "pricing": [
        "price", "cost", "how much", "premium"
    ],
    "ready_to_buy": [
        "ready", "sign up", "let’s do it", "call me"
    ],
    "emotional": [
        "worried", "afraid", "death", "accident"
    ],
}



def check_escalation(tenant, lead, message):
    text = message.lower()

    for reason, keywords in ESCALATION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                EscalationEvent.objects.create(
                    tenant=tenant,
                    lead=lead,
                    reason=reason,
                    triggered_by="rule"
                )
                return True, reason

    return False, None

def ai_confidence_check(ai_response):
    if "I might be mistaken" in ai_response:
        return True
    return False
