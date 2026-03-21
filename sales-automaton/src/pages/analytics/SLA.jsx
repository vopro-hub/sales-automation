import { useEffect, useState } from "react";
import { getSLA } from "./analyticsApi";
import "../../styles/sla.css";

export default function SLAAnalytics() {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    getSLA().then(res => setRows(res.data));
  }, []);

  return (
    <div className="sla-container">
      <h1 className="sla-title">SLA Violations</h1>

      <div className="sla-table-wrapper">
        <table className="sla-table">
          <thead>
            <tr>
              <th>Lead</th>
              <th>Agent</th>
              <th>Type</th>
              <th>Seconds Late</th>
            </tr>
          </thead>

          <tbody>
            {rows.map(v => (
              <tr key={v.id}>
                <td>{v.lead_id}</td>
                <td>{v.agent_email || "—"}</td>
                <td>{v.violation_type}</td>
                <td className={
                  v.seconds_late > 300
                    ? "sla-late-high"
                    : v.seconds_late > 120
                    ? "sla-late-medium"
                    : "sla-late-low"
                }>
                  {v.seconds_late}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}