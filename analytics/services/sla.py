from datetime import timedelta
from django.utils.timezone import now

def check_first_response_sla(lead):
    sla = lead.tenant.slaconfig
    elapsed = (now() - lead.created_at).seconds

    if elapsed > sla.max_first_response_seconds:
        SLAViolation.objects.create(
            tenant=lead.tenant,
            lead=lead,
            agent=lead.assigned_agent,
            violation_type="first_response",
            seconds_late=elapsed
        )
        notify_agent(
            lead.tenant,
            lead,
            reason="SLA violation: slow response"
        )


