import { useState, useEffect } from "react";
import api from "../../api/client";
import "../../styles/manualLeadCapture.css";
import useAuth from "../../hooks/hook";


export default function ManualLeadCapture() {

  const [agents, setAgents] = useState([]);
  const { user } = useAuth();
  const [notification, setNotification] = useState(null);

  const [form, setForm] = useState({
    name: "",
    phone: "",
    email: "",
    stage: "",
    notes: "",
    start_ai: true,
    assigned_agent_id: ""
  });

  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (user.role === "manager"){
      api.get("/leads/manual/lead/capture/")
      .then(res => {
        setAgents(res.data);
      });
   
    }
    

  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const submit = async (e) => {
    e.preventDefault();
  
    try {
      await api.post("leads/manual/lead/capture/", form);
  
      setNotification({
        type: "success",
        message: "Lead captured successfully!"
      });
  
      setForm({
        name: "",
        phone: "",
        email: "",
        stage: "",
        notes: "",
        start_ai: true,
        assigned_agent_id: ""
      });
  
    } catch (error) {
  
      setNotification({
        type: "error",
        message: "Failed to capture lead. Please try again."
      });
  
    }
  };

  if (!user) return null;

  return (
    <div className="manual-lead-page">

      <div className="manual-lead-card">

        <h2 className="manual-lead-title">Manual Lead Capture</h2>

        {notification && (
          <div>
            <div className={`notification ${notification.type}`}>
              <span>{notification.message}</span>
              <button
                className="close-btn"
                onClick={() => setNotification(null)}
              >
                ×
              </button>
            </div>
          </div>
          
        )}

        <input
          name="name"
          placeholder="Full Name"
          value={form.name}
          onChange={handleChange}
          required
        />

        <input
          name="phone"
          placeholder="Phone Number"
          value={form.phone}
          onChange={handleChange}
          required
        />

        <input
          name="email"
          placeholder="Email (optional)"
          value={form.email}
          onChange={handleChange}
        />

        <select
          name="stage"
          value={form.stage}
          onChange={handleChange}
          required
        >
          <option value="new">New</option>
          <option value="qualifying">Qualifying</option>
          <option value="qualified">Qualified</option>
        </select>

        
        {user.role === "manager" && (
          <select
            name="assigned_agent_id"
            value={form.assigned_agent_id}
            onChange={handleChange}
          >
            <option value="">Assign Agent (optional)</option>

            {agents.map(agent => (
              <option key={agent.id} value={agent.id}>
                {agent.name || agent.email}
              </option>
            ))}

          </select>
        )}

        <textarea
          name="notes"
          placeholder="Notes"
          value={form.notes}
          onChange={handleChange}
          required
        />

        <div className="aistart-checkbox">
          <label className="manual-checkbox">
             <input
               className="checkbox"
               type="checkbox"
               name="start_ai"
               checked={form.start_ai}
               onChange={handleChange}
             />
           </label>
           <span><small>Start AI qualification immediately</small></span>

        </div>

        <button
          className="manual-lead-btn"
          onClick={submit}
        >
          Save Lead
        </button>

      </div>

    </div>
  );
}