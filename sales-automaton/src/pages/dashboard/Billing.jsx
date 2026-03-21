import { useContext } from "react";
import { BillingContext } from "../../context/BillingContext";
import PricingCards from "../../components/PricingCards";

export default function Billing() {
  const billingContext = useContext(BillingContext);

  // SAFETY GUARD — prevents destructuring undefined
  if (!billingContext) {
    return (
      <div style={{ maxWidth: 1000, margin: "40px auto" }}>
        <h2>Billing</h2>
        <p>Billing context not available.</p>
      </div>
    );
  }

  const { billing, loading } = billingContext;

  if (loading) {
    return (
      <div style={{ maxWidth: 1000, margin: "40px auto" }}>
        <p>Loading billing…</p>
      </div>
    );
  }

  if (!billing || !billing.plan) {
    return (
      <div style={{ maxWidth: 1000, margin: "40px auto" }}>
        <h2>Plans</h2>
        <PricingCards currentPlan={null} />
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 1000, margin: "40px auto" }}>
      <h2>Billing & Subscription</h2>

      <div style={{ marginBottom: 30 }}>
        <h3>Current Plan</h3>

        <p>
          <b>{billing.plan.name}</b> —{" "}
          <span
            style={{
              color:
                billing.status === "active" ? "green" : "red",
              fontWeight: 500,
            }}
          >
            {billing.status}
          </span>
        </p>

        <p>
          Billing cycle:{" "}
          <b style={{ textTransform: "capitalize" }}>
            {billing.plan.billing_cycle}
          </b>
        </p>

        <p>
          Agents:{" "}
          {billing.usage?.agents ?? 0} /{" "}
          {billing.plan.max_agents}
        </p>

        <p>
          Leads this month:{" "}
          {billing.usage?.leads ?? 0} /{" "}
          {billing.plan.max_leads_per_month}
        </p>

        <p>
          Renewal date:{" "}
          {billing.current_period_end
            ? new Date(
                billing.current_period_end
              ).toLocaleDateString()
            : "—"}
        </p>
      </div>

      <PricingCards currentPlan={billing.plan.name} />
    </div>
  );
}
