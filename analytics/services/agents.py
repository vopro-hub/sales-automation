from django.db.models import Count
from leads.models import Lead
from bookings.models import BookingEvent
from analytics.models import SLAViolation


def get_agent_performance(tenant):
    agents = tenant.users.all()
    results = []

    for agent in agents:
        leads = Lead.objects.filter(
            tenant=tenant,
            assigned_agent=agent
        )

        bookings = BookingEvent.objects.filter(
            tenant=tenant,
            agent=agent,
            status="booked"
        )

        sla_count = SLAViolation.objects.filter(
            tenant=tenant,
            agent=agent
        ).count()

        lead_count = leads.count()
        booking_count = bookings.count()

        results.append({
            "name": agent.email,
            "leads": lead_count,
            "bookings": booking_count,
            "conversion_rate": round(
                (booking_count / lead_count) * 100, 2
            ) if lead_count else 0,
            "avg_response_time": 0,  # extend later
            "sla_violations": sla_count,
        })

    return results
