const express = require("express");
const wppconnect = require("@wppconnect-team/wppconnect");
const axios = require("axios");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.json());

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

/*
RANDOM HUMAN-LIKE DELAY
*/
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

  try {
    const QRCode = require("qrcode");
    
    sessions[session] = { client: null, qr: null };
    
    const client = await wppconnect.create({
      session: session,
      folderNameToken: SESSION_FOLDER,
      headless: true,
      useChrome: true,
      autoClose: 0,
      puppeteerOptions: {
        args: [
          "--no-sandbox",
          "--disable-setuid-sandbox",
          "--disable-dev-shm-usage"
        ]
      }
    });
    
    console.log("✅ CLIENT CREATED");
    
    // ✅ assign immediately
    sessions[session].client = client;
    
    /*
    QR EVENT (THIS FIXES YOUR PROBLEM)
    */
    client.on("qr", async (qr) => {
      console.log("✅ QR EVENT RECEIVED");
    
      try {
        const base64 = await QRCode.toDataURL(qr);
        sessions[session].qr = base64;
    
        console.log("QR STORED ✅");
      } catch (err) {
        console.error("QR conversion failed:", err);
      }
    });
    
    /*
    CONNECTED EVENT
    */
    client.onStateChange((state) => {
      console.log(`State change (${session}):`, state);
    
      if (state === "CONNECTED") {
        console.log("✅ WHATSAPP CONNECTED");
    
        // Optional: clear QR AFTER connection
        sessions[session].qr = null;
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
    HANDLE STATE CHANGES (AUTO RECONNECT)
    */
    client.onStateChange((state) => {
      console.log(`State change (${session}):`, state);

      if (
        state === "CONFLICT" ||
        state === "UNPAIRED" ||
        state === "UNLAUNCHED"
      ) {
        client.useHere();
      }
    });

    /*
    LISTEN FOR INCOMING MESSAGES
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

    res.json({ status: "session_started" });
  } catch (err) {
    console.error("Session start failed:", err);
    delete sessions[session];
    res.status(500).json({ error: err.message });
  }
});

/*
GET QR CODE
*/

app.get("/sessions/qr/:session", (req, res) => {
  const session = req.params.session;
  
  const s = sessions[session];

  if (!s) {
    return res.status(404).json({ error: "Session not found" });
  }

  return res.json({
    qr: s.qr,              // base64 image
    connected: !!s.client && !s.qr
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
SESSION STATUS
*/
app.get("/sessions/status", (req, res) => {
  const status = Object.keys(sessions).map((id) => ({
    session: id,
    connected: sessions[id].client ? true : false,
  }));

  res.json(status);
});

/*
HEALTH CHECK
*/
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    sessions: Object.keys(sessions).length,
  });
});

/*
AUTO RESTORE SESSIONS ON SERVER START
*/
async function restoreSessions() {
  try {
    const folders = fs.readdirSync(SESSION_FOLDER);

    for (const session of folders) {
      console.log("Restoring session:", session);

      sessions[session] = { client: null, qr: null };

      const client = await wppconnect.create({
        session: session,
        folderNameToken: SESSION_FOLDER,
        autoClose: 0,
        headless: true,
      });

      sessions[session].client = client;
    }
  } catch (err) {
    console.log("No previous sessions to restore");
  }
}

app.get("/debug/:session", (req, res) => {
  const session = req.params.session;

  if (!sessions[session]) {
    return res.status(404).json({ error: "Session not found" });
  }

  res.json({
    session,
    hasClient: !!sessions[session].client,
    qrExists: !!sessions[session].qr,
    qrPreview: sessions[session].qr
      ? sessions[session].qr.substring(0, 50)
      : null
  });
});

/*
START SERVER
*/
app.listen(PORT, async () => {
  console.log(`WPPConnect gateway running on port ${PORT}`);

  await restoreSessions();
});