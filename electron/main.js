const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let flaskProcess;

function createWindow() {
    const win = new BrowserWindow({
        width: 745,
        height: 600,
        autoHideMenuBar: true,
        resizable: false, 
        webPreferences: {
            nodeIntegration: false,
        },
    });

    // Point Electron window to Flask server
    win.loadURL("http://127.0.0.1:5000");
}

app.on("ready", () => {
    // Start Flask backend
    flaskProcess = spawn("python3", ["app.py"], {
        cwd: path.join(__dirname, ".."),
        shell: true,
    });

    flaskProcess.stdout.on("data", (data) => {
        console.log(`Flask: ${data}`);
    });

    flaskProcess.stderr.on("data", (data) => {
        console.error(`Flask Error: ${data}`);
    });

    createWindow();
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        if (flaskProcess) flaskProcess.kill();
        app.quit();
    }
});
