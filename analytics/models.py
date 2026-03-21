from django.db import models

class DailyMetrics(models.Model):
    tenant = models.ForeignKey("core.Tenant", on_delete=models.CASCADE)
    date = models.DateField()

    leads_received = models.IntegerField(default=0)
    leads_qualified = models.IntegerField(default=0)
    leads_booked = models.IntegerField(default=0)

    avg_first_response_seconds = models.IntegerField(default=0)
    avg_time_to_booking_seconds = models.IntegerField(default=0)

    ai_only_conversions = models.IntegerField(default=0)
    human_assisted_conversions = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tenant", "date")
        ordering =["-date"]
        
class SLAConfig(models.Model):
    tenant = models.OneToOneField("core.Tenant", on_delete=models.CASCADE)

    max_first_response_seconds = models.IntegerField(default=120)
    max_human_takeover_seconds = models.IntegerField(default=300)

class SLAViolation(models.Model):
    tenant = models.ForeignKey("core.Tenant", on_delete=models.CASCADE)
    lead = models.ForeignKey("leads.Lead", on_delete=models.CASCADE)
    agent = models.ForeignKey(
        "core.User",
        null=True,
        on_delete=models.SET_NULL
    )

    violation_type = models.CharField(max_length=50)
    seconds_late = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

