const { app, BrowserWindow } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 2000,
    height: 1000,
    webPreferences: {
      nodeIntegration: true
    }
  });

  win.loadURL('http://localhost:3000'); // ReactアプリケーションのURLをロード

  // 開発中にDevToolsを開く
  win.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});