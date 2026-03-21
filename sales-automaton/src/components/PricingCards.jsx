import { useEffect, useState } from "react";
import UpgradeButton from "./UpgradeButton";
import api from "../api/client";

export default function PricingCards({ currentPlan }) {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [billingCycle, setBillingCycle] = useState("monthly");
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const res = await api.get("/billing/plans/");
        setPlans(res.data || []);
      } catch (err) {
        setError("Unable to load pricing plans");
      } finally {
        setLoading(false);
      }
    };

    fetchPlans();
  }, []);
  
  if (loading) {
    return <p>Loading plans…</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>{error}</p>;
  }

  const calculatePrice = (plan) => {
    const base = Number(plan.price);

    if (billingCycle === "yearly") {
      const yearly = base * 12;
      const discount_percent = 100 - plan.discount;
      const discounted = yearly * discount_percent / 100;
      return {
        amount: discounted,
        original: yearly,
      };
    }

    return { amount: base };
  };

  return (
    <div>
      {/* ALERT IF NO PLAN */}
      {!currentPlan && (
        <div
          style={{
            background: "#fff3cd",
            border: "1px solid #ffeeba",
            padding: 16,
            marginBottom: 24,
            borderRadius: 6,
            color: "#856404",
          }}
        >
          <strong>No active subscription.</strong>  
          <div>
            Choose a plan below to activate automation, bookings, and AI sales.
          </div>
        </div>
      )}
      {/* BILLING CYCLE TOGGLE */}
      <div style={{ marginBottom: 24 }}>
        {["monthly", "yearly"].map((cycle) => (
          <button
            key={cycle}
            onClick={() => setBillingCycle(cycle)}
            style={{
              padding: "8px 16px",
              marginRight: 8,
              borderRadius: 6,
              border:
                billingCycle === cycle
                  ? "2px solid #4f46e5"
                  : "1px solid #ddd",
              background:
                billingCycle === cycle ? "#eef2ff" : "#fff",
              fontWeight: 500,
              textTransform: "capitalize",
            }}
          >
            {cycle}
          </button>
        ))}
      </div>
      <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
        {plans.map((plan) => {
          const isCurrent =
            currentPlan &&
            plan.name === currentPlan;
          const price = calculatePrice(plan);

          return (
            <div
              key={plan.id}
              style={{
                border: isCurrent
                  ? "2px solid #4f46e5"
                  : "1px solid #ddd",
                padding: 20,
                width: 300,
                borderRadius: 8,
                background: "#fff",
              }}
            >
              <h3>{plan.name}</h3>
              
              <h2>
                ${price.amount.toLocaleString()}{" "}
                <span style={{ fontSize: 14, fontWeight: 400 }}>
                  / {billingCycle}
                </span>
              </h2>

              {billingCycle === "yearly" && (
                <p
                  style={{
                    fontSize: 13,
                    color: "#16a34a",
                    marginTop: 4,
                  }}
                >
                  Save {plan.discount}% — ${price.original.toLocaleString()} / year
                </p>
              )}
              
              <ul>
                {(plan.features || []).map((feature) => (
                  <li key={feature}>{feature}</li>
                ))}
                <li>{plan.max_agents} Agent(s)</li>
                <li>{plan.max_leads} Leads</li>
              </ul>

              {isCurrent ? (
                <button disabled style={{ opacity: 0.6 }}>
                  Current Plan
                </button>
              ) : (
                <UpgradeButton plan={plan} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
