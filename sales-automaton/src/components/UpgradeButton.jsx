import { PAYSTACK_PUBLIC_KEY } from "../config/paystack";
import axios from "axios";
import { useContext } from "react";
import { BillingContext } from "../context/BillingContext";

export default function UpgradeButton({ plan }) {
  const { refreshBilling } = useContext(BillingContext);

  const pay = async () => {
    const res = await axios.post("/api/billing/paystack/init/", {
      plan: plan.name,
    });

    const handler = window.PaystackPop.setup({
      key: PAYSTACK_PUBLIC_KEY,
      email: res.data.email,
      amount: plan.price * 100,
      currency: "NGN",
      ref: res.data.reference,
      callback: async () => {
        await axios.post("/api/billing/paystack/verify/", {
          reference: res.data.reference,
        });
        await refreshBilling();
        alert("Payment successful. Plan upgraded.");
      },
    });

    handler.openIframe();
  };

  return <button onClick={pay}>Upgrade</button>;
}
