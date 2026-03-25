import { useState, useEffect } from "react";
import { io } from "socket.io-client";
import api from "../../api/client";
import QRCode from "qrcode";

const socket = io("http://localhost:3001");

export default function WhatsAppConnect() {
  const [qr, setQr] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hasSession, setHasSession] = useState(false);
  const [connected, setConnected] = useState(false);

  const [sessionId, setSessionId] = useState(null); // ✅ NEW (dynamic)

  /*
  START SESSION
  */
  const startSession = async (force = false) => {
    setLoading(true);

    try {
      const res = await api.post("/whatsapp/start/", {
        force
      });

      // ✅ NEW: get sessionId from backend
      const newSessionId = res.data.session_id;
      setSessionId(newSessionId);
      if (res.data.has_session && !force) {
        setHasSession(true);
        setLoading(false);
        return;
      }

    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  /*
  FETCH QR (FALLBACK)
  */
  const fetchQR = async () => {
    if (!sessionId) return; // ✅ NEW: prevent early calls

    try {
      const res = await api.get(`/whatsapp/qr/?session=${sessionId}`);

      if (res.data.qr) {
        setQr(res.data.qr);
      }

      if (res.data.connected) {
        setConnected(true);
        setQr(null);
      }

    } catch (err) {
      console.error(err);
    }
  };

  /*
  SOCKET LISTENERS (REAL-TIME)
  */
  useEffect(() => {
    if (!sessionId) return; // ✅ NEW

    const qrEvent = `qr:${sessionId}`;
    const connectedEvent = `connected:${sessionId}`;

    socket.on(qrEvent, (data) => {
      console.log("QR RECEIVED (socket)");
      setQr(data.qr);
      setConnected(false);
    });

    socket.on(connectedEvent, () => {
      console.log("CONNECTED");
      setConnected(true);
      setQr(null);
    });

    return () => {
      socket.off(qrEvent);
      socket.off(connectedEvent);
    };
  }, [sessionId]); // ✅ NEW dependency

  /*
  POLLING (FALLBACK SAFETY)
  */
  useEffect(() => {
    const interval = setInterval(fetchQR, 1000);
    return () => clearInterval(interval);
  }, [sessionId]); // ✅ UPDATED dependency

  return (
    <div style={{ padding: "20px" }}>
      <h2>Connect WhatsApp</h2>

      {!qr && !connected && !hasSession && !sessionId && (
        <button onClick={() => startSession()}>
          Scan to link your WhatsApp
        </button>
      )}

      {hasSession && !connected && (
        <div>
          <p>You already have a WhatsApp linked.</p>
          <button onClick={() => startSession(true)}>
            Relink WhatsApp
          </button>
        </div>
      )}

      {loading && <p>Loading...</p>}

      {qr && !connected && (
        <div>
          <p>Scan this QR with your WhatsApp</p>
          <img src={qr} alt="QR Code" style={{ width: "200px" }} />
        </div>
      )}

      {connected && (
        <div>
          <p style={{ color: "green", fontWeight: "bold" }}>
            ✅ WhatsApp Connected Successfully
          </p>
        </div>
      )}
    </div>
  );
}