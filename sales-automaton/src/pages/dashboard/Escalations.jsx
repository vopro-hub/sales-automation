import { useEffect, useState } from "react";
import { fetchEscalations } from "../../api/dashboard";
import "../../styles/escalations.css";

const Escalations = () => {

  const [items, setItems] = useState([]);

  useEffect(() => {

    const load = () => fetchEscalations().then(setItems);

    load();

    const interval = setInterval(load, 15000);
    return () => clearInterval(interval);

  }, []);

  return (

    <div className="escalations-page">

      <h1 className="escalations-title">Escalations</h1>

      {items.map((e, i) => (

        <div key={i} className="escalation-card">

          <div className="escalation-reason">
            {e.reason.toUpperCase()}
          </div>

          <div className="escalation-phone">
            {e.phone}
          </div>

          <div className="escalation-time">
            {new Date(e.created_at).toLocaleString()}
          </div>

        </div>

      ))}

    </div>

  );
};

export default Escalations;