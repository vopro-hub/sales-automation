import { useState, useEffect } from "react";
import api from "../../api/client";

export default function WhatsAppConnect() {
  const [qr, setQr] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hasSession, setHasSession] = useState(false);

  const startSession = async (force = false) => {
    setLoading(true);

    try {
      const res = await api.post("/whatsapp/start/", { force });

      if (res.data.has_session && !force) {
        setHasSession(true);
        setLoading(false);
        return;
      }

      fetchQR();

    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };
  
  useEffect(() => {
    const interval = setInterval(fetchQR, 2000);
    return () => clearInterval(interval);
  }, []);

  const fetchQR = async () => {
    const res = await api.get("/whatsapp/qr/");
    setQr(res.data.qr);
    console.log("qr:", res.data.qr);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Connect WhatsApp</h2>

      {!qr && !hasSession && (
        <button onClick={() => startSession()}>
          Scan to link your WhatsApp
        </button>
      )}

      {hasSession && (
        <div>
          <p>You already have a WhatsApp linked.</p>
          <button onClick={() => startSession(true)}>
            Relink WhatsApp
          </button>
        </div>
      )}

      {loading && <p>Loading...</p>}

      {qr && (
        <div>
          <p>Scan this QR with your WhatsApp</p>
          <img src={qr} alt="QR Code" style={{ width: "300px" }}/>
        </div>
      )}
    </div>
  );
}