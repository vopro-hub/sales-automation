import axios from "axios";

export default function AgentAssign({ lead, agents, refresh }) {
  const assign = async (agentId) => {
    await axios.post(`/api/leads/${lead.id}/assign/`, {
      agent_id: agentId,
    });
    refresh();
  };

  return (
    <select
      value={lead.assigned_agent?.id || ""}
      onChange={(e) => assign(e.target.value)}
    >
      <option value="">Unassigned</option>
      {agents.map((a) => (
        <option key={a.id} value={a.id}>
          {a.username}
        </option>
      ))}
    </select>
  );
}
