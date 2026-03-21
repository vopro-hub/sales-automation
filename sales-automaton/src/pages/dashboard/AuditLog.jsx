import { useEffect, useState } from "react";
import api from "../../api/client";
import "../../styles/auditLog.css";

export default function AuditLog() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    api.get("/audit-logs/").then((res) => {
      setLogs(res.data);
    });
  }, []);

  return (
    <div className="audit-page">
      <div className="audit-container">

        <h2 className="audit-title">Audit Log</h2>

        <div className="audit-table-wrapper">
          <table className="audit-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>User</th>
                <th>Action</th>
                <th>Object</th>
                <th>Message</th>
              </tr>
            </thead>

            <tbody>
              {logs.map((l) => (
                <tr key={l.id}>
                  <td>{new Date(l.created_at).toLocaleString()}</td>
                  <td>{l.user}</td>
                  <td>{l.action}</td>

                  <td className="audit-object">
                    {l.object_type} #{l.object_id}
                  </td>

                  <td className="audit-message">
                    {l.message}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
}