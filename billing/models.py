from django.db import models
from django.utils import timezone
from datetime import timedelta
from core.models import Tenant


class Plan(models.Model):
    
    name = models.CharField(max_length=50, default="Trial")
    price_monthly = models.DecimalField(max_digits=8, decimal_places=2)
    max_agents = models.IntegerField()
    max_leads_per_month = models.IntegerField()
    features = models.TextField()
    price_discount = models.IntegerField(default=0)

class Subscription(models.Model):
    BILLING_CYCLE_CHOICES = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    )
    STATUS_CHOICES = (
        ("active", "Active"),
        ("past_due", "Past Due"),
        ("cancelled", "Cancelled"),
    )
    tenant = models.OneToOneField("core.Tenant", on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField( max_length=20, choices=STATUS_CHOICES)
    amount_payable = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    billing_cycle = models.CharField( max_length=20, choices=BILLING_CYCLE_CHOICES, default="monthly")
    current_period_start = models.DateTimeField(default=timezone.now)
    current_period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.current_period_end:
            if self.billing_cycle == "monthly":
                self.current_period_end = self.current_period_start + timedelta(days=30)
                self.amount_payable=self.plan.price_monthly
            else:
                self.current_period_end = self.current_period_start + timedelta(days=365)
                cross_amount =self.plan.price_monthly * 12
                discount = cross_amount * self.plan.price_discount
                self.amount_payable=cross_amount - discount
        super().save(*args, **kwargs)

    def is_active(self):
        return self.status == "active" and self.current_period_end > timezone.now()

    def __str__(self):
        return f"{self.tenant.name} → {self.plan.name}"
    
    
class Invoice(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="invoices" )
    reference = models.CharField( max_length=100, unique=True, db_index=True)
    amount = models.DecimalField( max_digits=10, decimal_places=2 )
    currency = models.CharField( max_length=10, default="GHS")
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default="pending")
    issued_at = models.DateTimeField(default=timezone.now)
    paid_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-issued_at"]
        indexes = [ models.Index(fields=["tenant", "status"]),]

    def mark_paid(self):
        self.status = "paid"
        self.paid_at = timezone.now()
        self.save(update_fields=["status", "paid_at"])

    def __str__(self):
        return f"Invoice {self.reference} – {self.tenant.name}"

    