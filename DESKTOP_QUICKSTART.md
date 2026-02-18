# 🚀 Quick Start: Desktop Application

Get the Hidden Gems desktop app running in 5 minutes.

## ⚡ Ultra-Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Start in development mode
npm run dev
```

Done! The app will open automatically.

---

## 📋 Step-by-Step Setup

### Step 1: Install Rust (one-time only)

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### Step 2: Navigate to project

```bash
cd /Users/anishranga/Downloads/hidden-gems-fbla-2026-main
```

### Step 3: Install Node dependencies

```bash
npm install
```

(This installs Tauri CLI and other tools needed for development)

### Step 4: Start development

```bash
npm run dev
```

**What happens:**
- Flask backend starts on `http://localhost:5001`
- A native window opens showing your web app
- You can close window or Ctrl+C to stop

---

## 🏗️ Build for Distribution

### Build DMG for macOS

```bash
npm run build
```

Output: `src-tauri/target/release/bundle/dmg/Hidden\ Gems_1.0.0_x64.dmg`

**To share:** Send the `.dmg` file - just double-click to install.

### Build MSI for Windows

(Run this on a Windows machine)

```bash
npm run build
```

Output: `src-tauri/target/release/bundle/msi/Hidden\ Gems_1.0.0_x64.msi`

### Build AppImage for Linux

(Run this on a Linux machine)

```bash
npm run build
```

Output: `src-tauri/target/release/bundle/appimage/hidden-gems-desktop_1.0.0_amd64.AppImage`

---

## 🎯 What Just Happened?

You've converted your web app into a **native cross-platform desktop application**:

- ✅ Single executable (no browser tabs needed)
- ✅ Flask runs locally in the background
- ✅ All your existing features work exactly the same
- ✅ Can be installed like any other app
- ✅ Runs offline (everything is local)

## 📁 Project Structure

```
Your Project/
├── package.json              ← Node config (Tauri setup)
├── launcher.py              ← Python startup script
├── src-tauri/               ← Tauri code (Rust)
│   ├── Cargo.toml
│   ├── src/main.rs          ← Opens window, starts Flask
│   └── tauri.conf.json      ← App config
├── web/                     ← Flask app (UNCHANGED)
│   ├── app.py
│   ├── templates/
│   └── static/
├── src/                     ← Python code (UNCHANGED)
├── .venv/                   ← Virtual environment
├── hidden_gems.db           ← SQLite database
└── .env                     ← Secrets (GITIGNORED)
```

---

## 🔧 Development Tips

### Hot reload not working?

If CSS/JS don't update:

```bash
npm run dev  # Restart development
```

### Port 5001 already in use?

Kill the existing process:

```bash
lsof -i :5001
kill -9 <PID>
```

### Full debug output?

```bash
npm run debug
```

### Check if Flask is running

```bash
curl http://localhost:5001/login
```

---

## 📦 Distribution

### For your team:
1. Build the app: `npm run build`
2. Upload the DMG/MSI/AppImage to file sharing
3. Team members download and double-click to install

### For the public:
1. Create GitHub release
2. Upload DMG/MSI/AppImage
3. Share download link

---

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| "command not found: npm" | Install Node.js from nodejs.org |
| "Port 5001 in use" | `kill -9 $(lsof -t -i :5001)` |
| "Blank white window" | Wait 5 seconds, Flask is loading |
| "Python not found" | Ensure `.venv` exists: `python3 -m venv .venv` |
| Build fails on macOS | Install Xcode: `xcode-select --install` |

---

## 🎓 Next Steps

1. ✅ **Test locally**: `npm run dev` 
2. ✅ **Build first release**: `npm run build`
3. ✅ **Test the executable** on your machine
4. ✅ **Share with team** for feedback
5. ✅ **Publish** when ready

---

## 📚 Full Documentation

See [DESKTOP_APP_GUIDE.md](./DESKTOP_APP_GUIDE.md) for:
- Complete setup instructions
- Configuration options
- Cross-platform specifics
- Troubleshooting guide
- Distribution steps

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: ✅ Ready to build
