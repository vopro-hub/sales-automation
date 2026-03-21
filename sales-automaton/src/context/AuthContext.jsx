import { createContext, useEffect, useState } from "react";
import api from "../api/client";
import { useNavigate } from "react-router-dom";
import parseErrors from "../utils/parseErrors";

export const AuthContext = createContext();

export function AuthProvider({ children }) {

  const [user, setUser] = useState(null);
  const [billing, setBilling] = useState(null);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();


  const loadUser = async () => {

    const token = localStorage.getItem("access");

    if (!token) {
      setLoading(false);
      return;
    }

    try {

      const res = await api.get("/auth/me/");

      setUser(res.data);

    } catch {

      logout();

    } finally {

      setLoading(false);

    }
  };


  const login = async (email, password) => {

    try {

      const res = await api.post("/auth/login/", {
        email,
        password,
      });

      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      await loadUser();   // 👈 important

      navigate("/");

      return { success: true };

    } catch (error) {

      const parsed = parseErrors(error);

      return {
        success: false,
        validationErrors: parsed,
      };

    }

  };


  const signup = async (tenant_slug, payload) => {

    try {

      await api.post(`/auth/signup/${tenant_slug}/`, payload);

      await login(payload.email, payload.password);

      return { success: true };

    } catch (error) {

      const parsed = parseErrors(error);

      return {
        success: false,
        validationErrors: parsed,
      };

    }

  };


  const logout = () => {

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

    setUser(null);

    navigate("/login");

  };


  useEffect(() => {

    loadUser();

  }, []);


  return (
    <AuthContext.Provider
      value={{
        user,
        billing,
        login,
        signup,
        logout,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}