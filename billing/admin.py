from django.contrib import admin
from .models import Plan, Subscription, Invoice


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price_monthly",
        "price_discount",
        "max_agents",
        "max_leads_per_month",
        "features",
    )
    list_filter = ("price_discount", "name")
    search_fields = ("name",)
    ordering = ("price_monthly",)
    
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "features", "price_monthly", "price_discount"),
        }),
        ("Limits", {
            "fields": ("max_agents", "max_leads_per_month"),
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "plan",
        "amount_payable",
        "status",
        "billing_cycle",
        "current_period_start",
        "current_period_end",
    )
    list_filter = ("status", "plan", "billing_cycle")
    search_fields = ("tenant__name", "tenant__whatsapp_number")
    ordering = ("-current_period_end",)

    readonly_fields = (
        "tenant",
        "billing_cycle",
        "amount_payable",
        "current_period_start",
        "current_period_end",
        "created_at",
    )

    fieldsets = (
        ("Tenant", {
            "fields": ("tenant",),
        }),
        ("Plan", {
            "fields": ("plan", "status","billing_cycle"),
        }),
        ("Period", {
            "fields": ("current_period_start", "current_period_end"),
        }),
        ("Metadata", {
            "fields": ("created_at",),
        }),
    )

    def has_add_permission(self, request):
        # Subscriptions should be created via billing logic, not admin
        return False


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "amount",
        "status",
        "issued_at",
        "paid_at",
    )
    list_filter = ("status",)
    search_fields = ("tenant__name", "reference")
    ordering = ("-issued_at",)

    readonly_fields = (
        "tenant",
        "amount",
        "reference",
        "issued_at",
        "paid_at",
    )

    fieldsets = (
        ("Invoice", {
            "fields": ("tenant", "reference", "amount", "status"),
        }),
        ("Dates", {
            "fields": ("issued_at", "paid_at"),
        }),
    )

    def has_add_permission(self, request):
        # Invoices should be system-generated
        return False

