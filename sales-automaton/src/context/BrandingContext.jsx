import { createContext, useEffect, useState } from "react";
import axios from "axios";

export const BrandContext = createContext();

export function BrandProvider({ children }) {
  const [brand, setBrand] = useState(null);

  useEffect(() => {
    axios.get("/api/branding/").then((res) => {
      setBrand(res.data);
    });
  }, []);

  return (
    <BrandContext.Provider value={brand}>
      {children}
    </BrandContext.Provider>
  );
}
