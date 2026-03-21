import { useEffect, useState } from "react";
import { getAIImpact } from "./analyticsApi";
import "../../styles/aiimpact.css";

export default function AIImpact() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getAIImpact().then(res => setData(res.data));
  }, []);

  if (!data) {
    return <p className="aiimpact-loading">Loading AI impact...</p>;
  }

  return (
    <div className="aiimpact-container">
      <h1 className="aiimpact-title">AI Impact</h1>

      <div className="aiimpact-card">
        <p className="aiimpact-metric">
          AI-only conversions: {data.ai_only}
        </p>

        <p className="aiimpact-metric">
          Human-assisted: {data.human_assisted}
        </p>

        <p className="aiimpact-highlight">
          AI Contribution: {data.ai_percentage}%
        </p>
      </div>
    </div>
  );
}