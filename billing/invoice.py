import uuid
from .models import Invoice


def create_invoice_for_subscription(subscription):
    return Invoice.objects.create(
        tenant=subscription.tenant,
        reference=str(uuid.uuid4()),
        amount=subscription.amount_payable,
        status="pending",
        metadata={
            "plan": subscription.plan.name,
            "billing_cycle": subscription.billing_cycle,
        },
    )
