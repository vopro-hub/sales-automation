import { Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";

import Login from "./pages/auth/Login";
import Signup from "./pages/auth/Signup";
import DashboardLayout from "./layout/DashboardLayout";
import Overview from "./pages/dashboard/Overview";
import Escalations from "./pages/dashboard/Escalations";
import Leads from "./pages/dashboard/Leads";
import Billing from "./pages/dashboard/Billing";
import WhatsAppConnect from "./pages/dashboard/WhatsAppConnect";
import ManualLeadCapture from "./pages/dashboard/ManualLeadCapture";
import CsvImport from "./pages/dashboard/CsvImport";
import AuditLog from "./pages/dashboard/AuditLog";
import { BrandProvider } from "./context/BrandingContext";
import AnalyticsLayout from "./pages/analytics/AnalyticsLayout";
import AnalyticsOverview from "./pages/analytics/AnalyticsOverview";
import FunnelAnalytics from "./pages/analytics/Funnel";
import AgentAnalytics from "./pages/analytics/Agents";
import AIImpact from "./pages/analytics/AIImpact";
import SLAAnalytics from "./pages/analytics/SLA";
import TenantOnboardingForm from "./pages/tenant_onboarding";

function PrivateRoute({ children }) {
  const { user, loading } = useContext(AuthContext);
  if (loading) return null;
  return user ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrandProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup/:tenant_slug" element={<Signup />} />
        <Route path="/tenant/onboarding" element={<TenantOnboardingForm />} />

        <Route path="/" element={ <PrivateRoute> <DashboardLayout /> </PrivateRoute> }>
          <Route index element={<Overview />} />
          <Route path="/whatsapp" element={<WhatsAppConnect />} />
          <Route path="/leads" element={<Leads />} />
          <Route path="/leads/new" element={<ManualLeadCapture />} />
          <Route path="/escalations" element={<Escalations />} />
          <Route path="/leads/import" element={<CsvImport />} />
          <Route path="/billing" element={<Billing />} />
          <Route path="/logs" element={<AuditLog />} />
        </Route>
        <Route path="/analytics" element={<AnalyticsLayout />}>
          <Route index element={<AnalyticsOverview />} />
          <Route path="funnel" element={<FunnelAnalytics />} />
          <Route path="agents" element={<AgentAnalytics />} />
          <Route path="ai-impact" element={<AIImpact />} />
          <Route path="sla" element={<SLAAnalytics />} />
        </Route>
      </Routes>
    </BrandProvider>
  );
}
