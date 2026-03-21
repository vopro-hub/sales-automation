import { useState } from "react";
import api from "../api/client";
import "../styles/tenantOnboarding.css";

export default function TenantOnboardingForm() {

  const [form, setForm] = useState({
    name: "",
    brand_name: "",
    logo_url: "",
    primary_color: "#2563eb",
    whatsapp_number: "",
    whatsapp_sender_name: "",
    system_prompt: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const submit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError(null);

    try {
      await api.post("/tenants/onboard/", form);

      setSuccess("Tenant onboarded successfully");
      setForm({});

    } catch (err) {
      setError(err.response?.data?.detail || "Onboarding failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="onboard-page">

      <div className="onboard-card">

        <h2 className="onboard-title">Tenant Onboarding</h2>

        {error && <div className="onboard-error">{error}</div>}
        {success && <div className="onboard-success">{success}</div>}

        <form className="onboard-form" onSubmit={submit}>

          <input
            className="onboard-input"
            name="name"
            placeholder="Legal Business Name"
            onChange={handleChange}
            required
          />

          <input
            className="onboard-input"
            name="brand_name"
            placeholder="Brand Name (Optional)"
            onChange={handleChange}
          />

          <input
            className="onboard-input"
            name="logo_url"
            placeholder="Logo URL"
            onChange={handleChange}
          />

          <input
            className="onboard-color"
            name="primary_color"
            type="color"
            onChange={handleChange}
            value={form.primary_color}
          />

          <input
            className="onboard-input"
            name="whatsapp_number"
            placeholder="WhatsApp Number"
            onChange={handleChange}
            required
          />

          <input
            className="onboard-input"
            name="whatsapp_sender_name"
            placeholder="WhatsApp Sender Name"
            onChange={handleChange}
          />

          <textarea
            className="onboard-textarea onboard-full"
            name="system_prompt"
            placeholder="AI system prompt (tone, rules, brand voice)"
            rows={5}
            onChange={handleChange}
            required
          />

          <button className="onboard-button" disabled={loading}>
            {loading ? "Onboarding..." : "Create Tenant"}
          </button>

        </form>

      </div>

    </div>
  );
}