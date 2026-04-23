const { app, BrowserWindow, Tray, Menu, nativeImage, ipcMain } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let mainWindow = null;
let tray = null;
let backendProcess = null;

const isDev = !app.isPackaged;
const BACKEND_PORT = 8000;
const FRONTEND_PORT = 3000;

// ─── Backend Lifecycle ───────────────────────────────────────────────
function startBackend() {
  const backendDir = isDev
    ? path.resolve(__dirname, "..", "..")
    : path.resolve(process.resourcesPath, "backend");

  console.log("[JARVIS] Starting backend from:", backendDir);

  backendProcess = spawn(
    "python",
    ["-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", String(BACKEND_PORT)],
    {
      cwd: backendDir,
      shell: true,
      stdio: ["ignore", "pipe", "pipe"],
      env: { ...process.env },
    }
  );

  backendProcess.stdout.on("data", (data) => {
    console.log(`[BACKEND] ${data.toString().trim()}`);
  });

  backendProcess.stderr.on("data", (data) => {
    console.log(`[BACKEND] ${data.toString().trim()}`);
  });

  backendProcess.on("error", (err) => {
    console.error("[JARVIS] Failed to start backend:", err);
  });

  backendProcess.on("exit", (code) => {
    console.log(`[JARVIS] Backend process exited with code ${code}`);
  });
}

function stopBackend() {
  if (backendProcess) {
    console.log("[JARVIS] Stopping backend...");
    backendProcess.kill("SIGTERM");
    backendProcess = null;
  }
}

// ─── Wait for Backend to be ready ────────────────────────────────────
function waitForBackend(retries = 30) {
  return new Promise((resolve, reject) => {
    const http = require("http");
    let attempt = 0;

    const check = () => {
      attempt++;
      const req = http.get(`http://127.0.0.1:${BACKEND_PORT}/health`, (res) => {
        if (res.statusCode === 200) {
          console.log("[JARVIS] Backend is ready.");
          resolve();
        } else {
          retry();
        }
      });
      req.on("error", retry);
      req.setTimeout(1000, retry);
    };

    const retry = () => {
      if (attempt >= retries) {
        console.error("[JARVIS] Backend failed to start after retries.");
        resolve(); // Still open the window, user can debug
        return;
      }
      setTimeout(check, 1000);
    };

    check();
  });
}

// ─── Window Creation ─────────────────────────────────────────────────
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1100,
    minHeight: 700,
    frame: false,           // Borderless for that premium look
    transparent: false,
    backgroundColor: "#050608",
    icon: path.join(__dirname, "icon.png"),
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false,   // Allow localhost cross-origin
    },
    titleBarStyle: "hidden",
    titleBarOverlay: {
      color: "#050608",
      symbolColor: "#06b6d4",
      height: 36,
    },
    show: false,
  });

  // Load the Next.js app
  const url = isDev
    ? `http://localhost:${FRONTEND_PORT}`
    : `http://localhost:${FRONTEND_PORT}`;

  mainWindow.loadURL(url);

  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
    mainWindow.focus();
  });

  mainWindow.on("close", (e) => {
    // Minimize to tray instead of closing
    e.preventDefault();
    mainWindow.hide();
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

// ─── System Tray ─────────────────────────────────────────────────────
function createTray() {
  const iconPath = path.join(__dirname, "icon.png");
  let trayIcon;
  
  try {
    trayIcon = nativeImage.createFromPath(iconPath).resize({ width: 16, height: 16 });
  } catch {
    trayIcon = nativeImage.createEmpty();
  }
  
  tray = new Tray(trayIcon);
  tray.setToolTip("JARVIS — AI Assistant");

  const contextMenu = Menu.buildFromTemplate([
    {
      label: "Show JARVIS",
      click: () => {
        if (mainWindow) {
          mainWindow.show();
          mainWindow.focus();
        }
      },
    },
    { type: "separator" },
    {
      label: "Quit JARVIS",
      click: () => {
        stopBackend();
        app.exit(0);
      },
    },
  ]);

  tray.setContextMenu(contextMenu);
  tray.on("double-click", () => {
    if (mainWindow) {
      mainWindow.show();
      mainWindow.focus();
    }
  });
}

// ─── App Lifecycle ───────────────────────────────────────────────────
app.whenReady().then(async () => {
  console.log("[JARVIS] Application starting...");
  
  startBackend();
  await waitForBackend();
  
  createWindow();
  createTray();

  // IPC handlers for frameless window controls
  ipcMain.on("window-minimize", () => mainWindow?.minimize());
  ipcMain.on("window-maximize", () => {
    if (mainWindow?.isMaximized()) mainWindow.unmaximize();
    else mainWindow?.maximize();
  });
  ipcMain.on("window-close", () => mainWindow?.hide());
});

app.on("window-all-closed", () => {
  // Don't quit — JARVIS lives in the tray
});

app.on("before-quit", () => {
  stopBackend();
});

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});
