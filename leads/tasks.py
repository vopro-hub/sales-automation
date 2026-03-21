from celery import shared_task
from leads.models import Lead
from leads.followups import process_lead_followup


def start_ai_qualification(lead_id):
    lead = Lead.objects.get(id=lead_id)
    
    if lead.ai_status in ["paused", "completed"]:
         return

@shared_task
def run_followups():
    leads = Lead.objects.filter(
        stage__in=["qualifying", "qualified"]
    )

    for lead in leads:
        process_lead_followup(lead)
