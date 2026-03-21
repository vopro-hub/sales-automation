import { useEffect, useState } from "react";
import { getAgents } from "./analyticsApi";
import "../../styles/agents.css";

export default function AgentAnalytics() {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    getAgents().then(res => setAgents(res.data));
  }, []);

  return (
    <div className="agents-container">
      <h1 className="agents-title">Agent Performance</h1>

      <div className="agents-table-wrapper">
        <table className="agents-table">
          <thead>
            <tr>
              <th className="agents-left">Agent</th>
              <th className="agents-center">Leads</th>
              <th className="agents-center">Bookings</th>
              <th className="agents-center">Conversion</th>
              <th className="agents-center">Avg Response (sec)</th>
              <th className="agents-center">SLA</th>
            </tr>
          </thead>

          <tbody>
            {agents.length === 0 ? (
              <tr>
                <td colSpan="6" className="agents-empty">
                  No agent data available
                </td>
              </tr>
            ) : (
              agents.map((a) => (
                <tr key={a.name}>
                  <td className="agents-left">{a.name}</td>
                  <td className="agents-center">{a.leads}</td>
                  <td className="agents-center">{a.bookings}</td>
                  <td className="agents-center">{a.conversion_rate}%</td>
                  <td className="agents-center">{a.avg_response_time}</td>
                  <td className="agents-center">{a.sla_violations}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}