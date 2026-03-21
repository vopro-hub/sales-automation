from core.models import User
from leads.models import Lead

def auto_assign_agent(tenant, lead):
    agents = User.objects.filter(
        tenant=tenant,
        is_agent=True
    ).order_by("id")

    if not agents.exists():
        return

    last = (
        Lead.objects.filter(tenant=tenant, assigned_agent__isnull=False)
        .order_by("-created_at")
        .first()
    )

    if not last:
        lead.assigned_agent = agents.first()
    else:
        idx = list(agents).index(last.assigned_agent)
        lead.assigned_agent = agents[(idx + 1) % len(agents)]

    lead.save(update_fields=["assigned_agent"])
