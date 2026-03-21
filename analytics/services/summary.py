from django.db.models import Sum
from analytics.models import DailyMetrics


def get_summary(tenant):
    metrics = DailyMetrics.objects.filter(tenant=tenant)

    total = metrics.aggregate(
        leads_received=Sum("leads_received"),
        leads_qualified=Sum("leads_qualified"),
        leads_booked=Sum("leads_booked"),
        ai_only=Sum("ai_only_conversions"),
        human_assisted=Sum("human_assisted_conversions"),
    )

    received = total["leads_received"] or 0
    booked = total["leads_booked"] or 0

    return {
        "leads_received": received,
        "leads_qualified": total["leads_qualified"] or 0,
        "leads_booked": booked,
        "conversion_rate": round(
            (booked / received) * 100, 2
        ) if received else 0,
        "ai_only": total["ai_only"] or 0,
        "human_assisted": total["human_assisted"] or 0,
    }
