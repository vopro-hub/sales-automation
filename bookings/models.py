from django.db import models
from core.models import Tenant
from leads.models import Lead

class BookingConfig(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    booking_url = models.URLField()
    min_score_required = models.IntegerField(default=70)

    def __str__(self):
        return f"{self.tenant.name} Booking Config"

class BookingEvent(models.Model):
    STATUS_CHOICES = [
        ("link_sent", "Link Sent"),
        ("booked", "Booked"),
        ("cancelled", "Cancelled"),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


