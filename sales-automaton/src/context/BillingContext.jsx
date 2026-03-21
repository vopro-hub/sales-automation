import { createContext, useEffect, useState } from "react";
import axios from "axios";

export const BillingContext = createContext();

export function BillingProvider({ children }) {
  const [billing, setBilling] = useState(null);
  const [loading, setLoading] = useState(true);

  const refreshBilling = async () => {
    const res = await axios.get("/api/billing/status/");
    setBilling(res.data);
    setLoading(false);
  };

  useEffect(() => {
    refreshBilling();
  }, []);

  return (
    <BillingContext.Provider
      value={{ billing, setBilling, setLoading, loading, refreshBilling }}
    >
      {children}
    </BillingContext.Provider>
  );
}
