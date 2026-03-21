from django.db import models
from core.models import Tenant
from django.conf import settings

class Lead(models.Model):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"

    LEAD_STATUS = [
        (HOT, "Hot"),
        (WARM, "Warm"),
        (COLD, "Cold"),
    ]
    SOURCE_CHOICES = [
        ("whatsapp", "WhatsApp"),
        ("manual", "Manual"),
        ("import", "Import"),
    ]
    AI_STATUS_CHOICES = [
        ("idle", "Idle"),
        ("running", "Running"),
        ("paused", "Paused"),
        ("completed", "Completed"),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.CharField(blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    status = models.CharField(max_length=10, choices=LEAD_STATUS, default=COLD)
    stage = models.CharField(max_length=20, default="new" ) # new | qualifying | qualified
    score = models.IntegerField(default=0)
    ai_status = models.CharField(max_length=20, choices=AI_STATUS_CHOICES, default="idle")
    ai_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_agent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="leads" )

    class Meta:
        unique_together = ("tenant", "phone", "email")

class Message(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    sender = models.CharField(max_length=10) # "lead" or "ai"
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Qualification(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)

    intent = models.CharField(max_length=100, blank=True, null=True)
    urgency = models.CharField(max_length=50, blank=True, null=True)
    decision_maker = models.BooleanField(null=True)
    coverage_amount = models.IntegerField(null=True)

    completed = models.BooleanField(default=False)

class FollowUpConfig(models.Model):
    tenant = models.OneToOneField("core.Tenant", on_delete=models.CASCADE)
    # delays in hours
    step_1_delay = models.IntegerField(default=24)
    step_2_delay = models.IntegerField(default=72)
    step_3_delay = models.IntegerField(default=168)

    is_active = models.BooleanField(default=True)

class FollowUpState(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    step_1_sent = models.BooleanField(default=False)
    step_2_sent = models.BooleanField(default=False)
    step_3_sent = models.BooleanField(default=False)

    completed = models.BooleanField(default=False)

class EscalationEvent(models.Model):
    tenant = models.ForeignKey("core.Tenant", on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    assigned_agent = models.CharField(null=True, blank=True)
    reason = models.CharField(max_length=100)
    triggered_by = models.CharField(
        max_length=20  # ai | rule
    )

    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
