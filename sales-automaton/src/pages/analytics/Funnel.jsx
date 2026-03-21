import { useEffect, useState } from "react";
import { getFunnel } from "./analyticsApi";
import "../../styles/funnel.css";

export default function FunnelAnalytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getFunnel().then(res => setData(res.data));
  }, []);

  if (!data) return <p className="funnel-loading">Loading funnel...</p>;

  return (
    <div className="funnel-container">
      <h1 className="funnel-title">Sales Funnel</h1>

      <div className="funnel-card">
        <ul className="funnel-list">

          <li className="funnel-item">
            <span className="funnel-label">Received</span>
            <span className="funnel-value">{data.received}</span>
          </li>

          <li className="funnel-item">
            <span className="funnel-label">Qualified</span>
            <span className="funnel-value">{data.qualified}</span>
          </li>

          <li className="funnel-item">
            <span className="funnel-label">Booked</span>
            <span className="funnel-value">{data.booked}</span>
          </li>

          <li className="funnel-item funnel-conversion">
            <span>Conversion Rate</span>
            <span>{data.conversion_rate}%</span>
          </li>

        </ul>
      </div>
    </div>
  );
}