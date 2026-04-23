const { contextBridge, ipcRenderer } = require("electron");

// Expose safe APIs to the renderer (frontend)
contextBridge.exposeInMainWorld("electronAPI", {
  platform: process.platform,
  isElectron: true,
  
  // Window controls for the frameless window
  minimize: () => ipcRenderer.send("window-minimize"),
  maximize: () => ipcRenderer.send("window-maximize"),
  close: () => ipcRenderer.send("window-close"),
});
