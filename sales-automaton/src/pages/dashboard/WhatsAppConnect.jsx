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

  const sessionId = "default"; // 🔥 IMPORTANT: must match backend session

  /*
  START SESSION
  */
  const startSession = async (force = false) => {
    setLoading(true);

    try {
      const res = await api.post("/whatsapp/start/", {
        session: sessionId,
        force
      });

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
    try {
      const res = await api.get(`/whatsapp/qr/?session=${sessionId}`);
      console.log("session is:", res.data.qr)
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
    socket.on(`qr:${sessionId}`, (data) => {
      console.log("QR RECEIVED (socket)");
      setQr(data.qr);
      setConnected(false);
    });

    socket.on(`connected:${sessionId}`, () => {
      console.log("CONNECTED");
      setConnected(true);
      setQr(null);
    });

    return () => {
      socket.off(`qr:${sessionId}`);
      socket.off(`connected:${sessionId}`);
    };
  }, []);

  /*
  POLLING (FALLBACK SAFETY)
  */
  useEffect(() => {
    const interval = setInterval(fetchQR, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Connect WhatsApp</h2>

      {!qr && !connected && !hasSession && (
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