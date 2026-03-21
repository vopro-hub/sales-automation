from datetime import date
from django.db.models import Avg
from leads.models import Lead
from bookings.models import BookingEvent
from analytics.models import DailyMetrics

def generate_daily_metrics():
    today = date.today()

    for tenant in Tenant.objects.all():
        leads = Lead.objects.filter(
            tenant=tenant,
            created_at__date=today
        )

        bookings = BookingEvent.objects.filter(
            tenant=tenant,
            status="booked",
            created_at__date=today
        )

        DailyMetrics.objects.update_or_create(
            tenant=tenant,
            date=today,
            defaults={
                "leads_received": leads.count(),
                "leads_qualified": leads.filter(stage="qualified").count(),
                "leads_booked": bookings.count(),
            }
        )
