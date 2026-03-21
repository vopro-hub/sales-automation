import { useEffect, useState } from "react";
import { fetchOverview } from "../../api/dashboard";
import "../../styles/overview.css";

const Overview = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = () => {
      fetchOverview()
        .then(setData)
        .finally(() => setLoading(false));
    };

    loadData();
    const interval = setInterval(loadData, 30000);

    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="overview-loading">Loading system metrics...</div>;
  if (!data) return <div className="overview-error">Error loading metrics</div>;

  return (
    <div className="overview-container">
      <h1 className="overview-title">System Overview</h1>

      <div className="metrics-grid">
        <Metric label="Leads Today" value={data.leads_today} />
        <Metric label="Qualified Leads" value={data.qualified_leads} />
        <Metric label="Bookings" value={data.bookings} />
        <Metric label="Active Escalations" value={data.escalations} />
      </div>
    </div>
  );
};

const Metric = ({ label, value, alert }) => (
  <div className={`metric-card ${alert ? "metric-alert" : ""}`}>
    <div className="metric-label">{label}</div>
    <div className="metric-value">{value}</div>

    {alert && <span className="alert-dot" />}
  </div>
);

export default Overview;