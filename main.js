const { app, BrowserWindow, dialog, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const pdf = require('pdf-parse');
const mammoth = require('mammoth');
const say = require('say');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });
  mainWindow.loadFile(path.join(__dirname, 'app', 'index.html'));
}

app.whenReady().then(createWindow);

ipcMain.handle('open-file', async () => {
  const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
    filters: [
      { name: 'Documents', extensions: ['txt', 'pdf', 'docx'] }
    ],
    properties: ['openFile']
  });
  if (canceled || !filePaths.length) return { text: null };
  const filePath = filePaths[0];
  if (filePath.endsWith('.txt')) {
    const text = fs.readFileSync(filePath, 'utf8');
    return { text };
  } else if (filePath.endsWith('.pdf')) {
    const dataBuffer = fs.readFileSync(filePath);
    const data = await pdf(dataBuffer);
    return { text: data.text };
  } else if (filePath.endsWith('.docx')) {
    const result = await mammoth.extractRawText({ path: filePath });
    return { text: result.value };
  }
  return { text: null };
});

ipcMain.handle('speak', (_, text, opts) => {
  say.speak(text, opts?.voice || null, opts?.speed || 1.0);
});

ipcMain.handle('stop-speech', () => {
  say.stop();
});

ipcMain.handle('get-voices', () => {
  return new Promise((resolve) => {
    say.getInstalledVoices((err, voices) => {
      if (err) resolve([]); else resolve(voices);
    });
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
