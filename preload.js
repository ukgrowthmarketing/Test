const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  openFile: () => ipcRenderer.invoke('open-file'),
  speak: (text, opts) => ipcRenderer.invoke('speak', text, opts),
  stop: () => ipcRenderer.invoke('stop-speech'),
  getVoices: () => ipcRenderer.invoke('get-voices')
});
