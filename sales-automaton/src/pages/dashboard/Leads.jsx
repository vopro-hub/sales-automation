import { useEffect, useState } from "react";
import { fetchLeads } from "../../api/dashboard";
import AiControls from "../../components/AiControls";
import AgentAssign from "../../components/AgentAssign";
import "../../styles/leads.css";

const Leads = () => {
  const [leads, setLeads] = useState([]);

  useEffect(() => {
    const load = () => fetchLeads().then(setLeads);

    load();

    const interval = setInterval(load, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="leads-page">

      <h1 className="leads-title">Leads</h1>

      <div className="leads-table-wrapper">

        <table className="leads-table">

          <thead>
            <tr>
              <th>Tenant</th>
              <th>Phone</th>
              <th>Stage</th>
              <th>Score</th>
              <th>Created</th>
              <th>Agent</th>
              <th>AI</th>
            </tr>
          </thead>

          <tbody>
            {leads.map((lead, i) => (

              <tr
                key={i}
                className={lead.stage === "qualified" ? "lead-qualified" : ""}
              >

                <td>{lead.tenant}</td>

                <td>{lead.phone}</td>

                <td>
                  <span className="stage-badge">
                    {lead.stage}
                  </span>
                </td>

                <td>
                  <span className="score-badge">
                    {lead.score}
                  </span>
                </td>

                <td>
                  {new Date(lead.created_at).toLocaleString()}
                </td>

                <td>
                  <AgentAssign
                    lead={lead}
                    agents={agents}
                    refresh={fetchLeads}
                  />
                </td>

                <td>
                  <AiControls
                    lead={lead}
                    refresh={fetchLeads}
                  />
                </td>

              </tr>

            ))}
          </tbody>

        </table>

      </div>

    </div>
  );
};

export default Leads;