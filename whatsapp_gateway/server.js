const express = require("express");
const wppconnect = require("@wppconnect-team/wppconnect");
const axios = require("axios");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
app.use(express.json());

/*
SERVER + SOCKET SETUP (FIXED)
*/
const server = http.createServer(app);

const io = new Server(server, {
  cors: { origin: "*" }
});

/*
SESSION STORE
*/
const sessions = {};

/*
CONFIG
*/
const PORT = 3001;
const DJANGO_WEBHOOK = "http://localhost:8000/api/whatsapp/webhook/";
const SECRET = "super-secure-webhook-secret";

/*
SESSION STORAGE DIRECTORY
*/
const SESSION_FOLDER = path.join(__dirname, "sessions");

if (!fs.existsSync(SESSION_FOLDER)) {
  fs.mkdirSync(SESSION_FOLDER);
}

/*
ANTI BAN SETTINGS
*/
const MIN_DELAY = 2000;
const MAX_DELAY = 5000;

function randomDelay() {
  const delay = Math.floor(
    Math.random() * (MAX_DELAY - MIN_DELAY) + MIN_DELAY
  );
  return new Promise((resolve) => setTimeout(resolve, delay));
}

/*
START SESSION
*/
app.post("/sessions/start", async (req, res) => {
  const { session } = req.body;

  if (!session) {
    return res.status(400).json({ error: "Session ID required" });
  }

  if (sessions[session]) {
    return res.json({ status: "session_already_running" });
  }

  // 🔥 Respond immediately (prevents frontend hanging)
  res.json({ status: "starting" });

  try {
    sessions[session] = {
      client: null,
      qr: null,
      connected: false
    };

    const client = await wppconnect.create({
      session: session,
      folderNameToken: SESSION_FOLDER,
      headless: true,
      autoClose: 0,

      puppeteerOptions: {
        args: ["--no-sandbox", "--disable-setuid-sandbox"]
      },

      // ✅ ONLY QR HANDLER YOU NEED
      catchQR: async (qr) => {
        console.log("✅ QR RECEIVED");
        sessions[session].qr = qr;

        io.emit(`qr:${session}`, { qr });
        //const QRCode = require("qrcode");
        //const base64 = await QRCode.toDataURL(qr);

        //sessions[session].qr = base64;

        //io.emit(`qr:${session}`, { qr: base64 });
      },

      statusFind: (status) => {
        console.log("STATUS:", status);
      }
    });

    console.log("✅ CLIENT CREATED");

    sessions[session].client = client;

    /*
    STATE CHANGE
    */
    client.onStateChange((state) => {
      console.log(`STATE (${session}):`, state);

      if (state === "CONNECTED") {
        sessions[session].connected = true;
        // 🔥 CALL DJANGO TO SAVE SESSION
        axios.post("http://localhost:8000/api/whatsapp/connected/", {
          session_id: session
        }).catch(err => {
          console.error("Failed to notify Django:", err.message);
        });
        sessions[session].qr = null;

        io.emit(`connected:${session}`, {
          connected: true
        });

        console.log("✅ WHATSAPP CONNECTED");
      }

      if (
        state === "CONFLICT" ||
        state === "UNPAIRED" ||
        state === "UNLAUNCHED"
      ) {
        client.useHere();
      }
    });

    /*
    INCOMING MESSAGES
    */
    client.onMessage(async (message) => {
      try {
        if (message.isGroupMsg) return;
        if (!message.body) return;

        const payload = {
          session: session,
          from: message.from,
          body: message.body,
          isGroupMsg: message.isGroupMsg,
        };

        const signature = crypto
          .createHmac("sha256", SECRET)
          .update(JSON.stringify(payload))
          .digest("hex");

        await axios.post(DJANGO_WEBHOOK, payload, {
          headers: {
            "X-WPP-Signature": signature,
          },
          timeout: 5000,
        });
      } catch (err) {
        console.error("Webhook delivery failed:", err.message);
      }
    });

  } catch (err) {
    console.error("Session start failed:", err);
    delete sessions[session];
  }
});

/*
GET QR
*/
app.get("/sessions/qr/:session", (req, res) => {
  const s = sessions[req.params.session];

  if (!s) {
    return res.status(404).json({ error: "Session not found" });
  }

  res.json({
    qr: s.qr,
    connected: s.connected
  });
});

/*
SEND MESSAGE
*/
app.post("/messages/send", async (req, res) => {
  const { session, to, message } = req.body;

  const s = sessions[session];

  if (!s || !s.client) {
    return res.status(404).json({ error: "Session not active" });
  }

  try {
    await randomDelay();

    const number = to.includes("@c.us") ? to : `${to}@c.us`;

    await s.client.sendText(number, message);

    res.json({ status: "sent" });
  } catch (err) {
    console.error("Send message failed:", err);
    res.status(500).json({ error: err.message });
  }
});

/*
HEALTH
*/
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

/*
START SERVER
*/
server.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});