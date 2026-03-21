import axios from "axios";

export default function AiControls({ lead, refresh }) {
  const action = async (type) => {
    await axios.post(`/api/leads/${lead.id}/ai/${type}/`);
    refresh();
  };

  if (lead.ai_status === "idle") {
    return <button onClick={() => action("start")}>Start AI</button>;
  }

  if (lead.ai_status === "running") {
    return <button onClick={() => action("pause")}>Pause AI</button>;
  }

  if (lead.ai_status === "paused") {
    return <button onClick={() => action("resume")}>Resume AI</button>;
  }

  return <span>Completed</span>;
}
