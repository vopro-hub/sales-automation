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
const DJANGO_WEBHOOK = "http://127.0.0.1:8000/api/whatsapp/webhook/";
const SECRET = "super-secure-webhook-secret";

/*
SESSION STORAGE DIRECTORY
*/
const SESSION_FOLDER = "/home/abaviawe/wpp-sessions";

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

let browserInstance = null;

/*
🔥 WARMUP BROWSER
*/
async function warmupWPP() {
  try {
    console.log("🔥 Starting persistent browser...");

    browserInstance = await wppconnect.create({
      session: "engine",
      headless: true,
      autoClose: 0,
      useChrome: true,
      puppeteerOptions: {
        args: ["--no-sandbox", "--disable-setuid-sandbox"]
      },
      catchQR: () => {},
      statusFind: () => {}
    });

    console.log("✅ Browser ready (persistent)");

  } catch (err) {
    console.error("❌ Warmup failed:", err.message);
  }
}

/*
🔥 ATTACH LISTENERS (REUSABLE)
*/
function attachListeners(client, session) {

  client.onStateChange((state) => {
    console.log(`STATE (${session}):`, state);

    if (state === "CONNECTED") {
      sessions[session].connected = true;

      axios.post("http://localhost:8000/api/whatsapp/connected/", {
        session_id: session
      },
      {
        headers: {
          Authorization: `Bearer ${sessions[session].token}`
        }
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

    // 🔥 AUTO RECONNECT
    if (state === "DISCONNECTED") {
      console.log(`♻️ Reconnecting session: ${session}`);
      client.initialize();
    }
  });

  client.onMessage(async (message) => {
    try {
      if (message.isGroupMsg) return;
      if (!message.body) return;

      const sender =
        message.from ||
        message.sender?.id ||
        message.chatId ||
        message.chat?.id;

      if (!sender) {
        console.log("⚠️ No sender found:", message);
        return;
      }

      console.log("📩 INCOMING FROM:", sender);

      const payload = {
        session: session,
        from: sender,
        body: message.body,
        isGroupMsg: message.isGroupMsg,
      };

      const signature = crypto
        .createHmac("sha256", SECRET)
        .update(JSON.stringify(payload))
        .digest("hex");

      const response = await axios.post(DJANGO_WEBHOOK, payload, {
        headers: {
          "X-WPP-Signature": signature,
        },
        timeout: 5000,
      });

      console.log("✅ DJANGO RESPONSE:", response.status);

    } catch (err) {
      console.error("❌ ERROR STATUS:", err.response?.status);
      console.error("❌ ERROR DATA:", err.response?.data);
    }
  });
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

  res.json({ status: "starting" });

  try {
    sessions[session] = {
      client: null,
      qr: null,
      connected: false,
      token: req.body.token
    };

    const client = await wppconnect.create({
      session: session,
      folderNameToken: "tokens",
      mkdirFolderToken: SESSION_FOLDER,
      persistSession: true,
      headless: true,
      autoClose: 0,
      useChrome: true,

      //browserWSEndpoint: browserInstance?.puppeteer?.wsEndpoint?.(),
      createOptions: {
        browserArgs: ["--no-sandbox", "--disable-setuid-sandbox"],
        devtools: false,
      },
      puppeteerOptions: {
        userDataDir: path.join(SESSION_FOLDER, session),
      },

      catchQR: async (qr) => {
        console.log("✅ QR RECEIVED");
        sessions[session].qr = qr;

        io.emit(`qr:${session}`, { qr });
      },

      statusFind: (status) => {
        console.log("STATUS:", status);
      }
    });

    console.log("✅ CLIENT CREATED");

    sessions[session].client = client;

    // 🔥 ATTACH LISTENERS
    attachListeners(client, session);

  } catch (err) {
    console.error("Session start failed:", err);
    delete sessions[session];
  }
});

/*
🔥 RESTORE SESSIONS (PERSISTENCE FIX)
*/
async function restoreSessions() {
  try {
    const storedSessions = fs.readdirSync(SESSION_FOLDER);

    for (const session of storedSessions) {
      console.log("🔄 Restoring session:", session);

      sessions[session] = {
        client: null,
        qr: null,
        connected: false,
        token: null
      };

      const client = await wppconnect.create({
        session: session,
        folderNameToken: SESSION_FOLDER,
        persistSession: true,
        headless: true,
        autoClose: 0,
        useChrome: true,

        //browserWSEndpoint: browserInstance?.puppeteer?.wsEndpoint?.(),

        puppeteerOptions: {
          userDataDir: path.join(SESSION_FOLDER, session),
          args: ["--no-sandbox", "--disable-setuid-sandbox"]
        },

        catchQR: () => {},
        statusFind: (status) => {
          console.log(`RESTORE STATUS (${session}):`, status);
        }
      });

      sessions[session].client = client;

      // 🔥 REATTACH LISTENERS
      attachListeners(client, session);

      console.log("✅ Restored session:", session);
    }

  } catch (err) {
    console.log("ℹ️ No sessions to restore");
  }
}

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

  const delay = Math.min(3000, message.length * 100);

  try {
    await randomDelay();

    await s.client.sendSeen(to);
    await s.client.startTyping(to);
    await new Promise(resolve => setTimeout(resolve, delay));
    await s.client.sendText(to, message);
    await s.client.stopTyping(to);

    console.log("✅ MESSAGE SENT");

    res.json({ status: "sent" });

  } catch (err) {
    console.error("Send message failed:", err);

    try {
      await s.client.stopTyping(to);
    } catch (e) {}

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
server.listen(PORT, async () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);

  await warmupWPP();

  // 🔥 THIS IS THE KEY ADDITION
  await restoreSessions();

  await browserInstance.getWAVersion();
});