import { useEffect, useState } from "react";
import { getSummary } from "./analyticsApi";
import "../../styles/analyticsOverview.css";

export default function AnalyticsOverview() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getSummary().then(res => setData(res.data));
  }, []);

  if (!data) return <p className="analytics-loading">Loading analytics...</p>;

  return (
    <div className="analytics-overview">
      <h1 className="analytics-title">
        Analytics Overview
      </h1>

      <div className="metrics-grid">
        <Metric title="Leads Received" value={data.leads_received} />
        <Metric title="Leads Qualified" value={data.leads_qualified} />
        <Metric title="Bookings" value={data.leads_booked} />
        <Metric title="Conversion Rate" value={`${data.conversion_rate}%`} />
        <Metric title="AI Only Conversions" value={data.ai_only} />
        <Metric title="Human Assisted" value={data.human_assisted} />
      </div>
    </div>
  );
}

function Metric({ title, value }) {
  return (
    <div className="metric-card">
      <p className="metric-title">{title}</p>
      <p className="metric-value">{value}</p>
    </div>
  );
}