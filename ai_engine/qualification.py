from leads.models import Lead, Qualification
from bookings.logic import try_send_booking_link
from celery import shared_task

@shared_task
def start_ai_qualification(lead_id):
    lead = Lead.objects.get(id=lead_id)

    if lead.ai_status != "running":
        return


def update_qualification(lead, message):
    q, _ = Qualification.objects.get_or_create(lead=lead)

    text = message.lower()

    if "family" in text:
        q.intent = "family_protection"

    if "now" in text or "urgent" in text:
        q.urgency = "immediate"

    if "i decide" in text or "my decision" in text:
        q.decision_maker = True

    q.save()

    calculate_score(lead, q)

def calculate_score(lead, q):
    score = 0

    if q.intent:
        score += 20
    if q.urgency == "immediate":
        score += 40
    if q.decision_maker:
        score += 30

    lead.score = score

    if score >= 70:
        lead.stage = "qualified"
        lead.status = "hot"
        try_send_booking_link(lead)
    else:
        lead.stage = "qualifying",
        lead.status = "warm"
    lead.save()
