# 🖥️ Hidden Gems Desktop Application

Converting Hidden Gems from a web app to a native desktop application.

## Overview

The desktop version bundles the existing Flask backend with a Tauri wrapper for maximum efficiency:

- **Frontend**: Your existing HTML/CSS/JavaScript web UI
- **Backend**: Flask running locally at `http://localhost:5001`
- **Desktop Framework**: Tauri (lightweight, ~60MB vs 200MB+ Electron)
- **Platforms Supported**: Windows, macOS, Linux
- **Database**: SQLite bundled with the app

## Architecture

```
Hidden Gems Desktop App
├── Tauri Window (Rust)
│   ├── Runs Flask backend in background
│   ├── Opens window pointing to localhost:5001
│   └── Handles windowing & OS integration
├── Flask Backend (Python)
│   ├── .venv (virtual environment)
│   ├── web/ (Flask app code)
│   ├── src/ (database, logic, auth)
│   └── hidden_gems.db (SQLite database)
└── User Data
    ├── .env (secrets - not bundled)
    └── Config files
```

## Setup Instructions

### Prerequisites

1. **Node.js & npm** (Node 16+)
   ```bash
   npm --version  # Should be 8+
   ```

2. **Rust** (for building Tauri)
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

3. **Python 3.8+** (already set up)
   ```bash
   python3 --version
   ```

### Installation

#### 1. Install Tauri CLI
```bash
cd /Users/anishranga/Downloads/hidden-gems-fbla-2026-main
npm install
```

#### 2. Install additional dependencies
```bash
npm install -D @tauri-apps/cli @tauri-apps/api
```

#### 3. Configure environment
```bash
cp .env.example .env  # Configure SMTP, GROQ_API_KEY, etc.
```

#### 4. Build Python virtual environment
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Development

#### Run in development mode
```bash
npm run dev
```

This will:
1. Start the Flask backend on port 5001
2. Open a Tauri window displaying the app
3. Enable hot-reload (CSS/JS changes refresh immediately)
4. Show debug console for errors

#### Debug issues
```bash
npm run debug  # Verbose output with full error traces
```

### Building for Distribution

#### macOS DMG
```bash
npm run build
# Output: src-tauri/target/release/bundle/dmg/Hidden\ Gems_1.0.0_x64.dmg
```

#### Windows MSI
```bash
npm run build
# Output: src-tauri/target/release/bundle/msi/Hidden\ Gems_1.0.0_x64.msi
```

#### Linux AppImage
```bash
npm run build
# Output: src-tauri/target/release/bundle/appimage/hidden-gems-desktop_1.0.0_amd64.AppImage
```

## File Structure

```
hidden-gems-fbla-2026-main/
├── package.json              # Tauri/Node config
├── src-tauri/               # Tauri (Rust) code
│   ├── Cargo.toml          # Rust dependencies
│   ├── src/
│   │   └── main.rs         # Main Tauri entry point
│   └── tauri.conf.json     # Tauri config
├── web/                     # Flask app (unchanged)
│   ├── app.py
│   ├── templates/
│   ├── static/
│   └── __init__.py
├── src/                     # Python logic (unchanged)
│   ├── database/
│   ├── logic/
│   └── verification/
├── .venv/                   # Python virtual environment
├── hidden_gems.db           # SQLite database
└── .env                     # Environment secrets
```

## Key Features

✅ **Single clickable executable** - No terminal needed
✅ **Local database** - Cannot be lost (always with app)
✅ **Auto-start Flask** - User doesn't manage backend
✅ **Native OS integration** - File dialogs, notifications, system tray
✅ **Offline capable** - Entire app runs locally
✅ **Fast startup** - ~2 seconds (vs web app loading)
✅ **Cross-platform** - Same executable builds for all OSs

## Troubleshooting

### "Command not found: tauri"
Solution: Install Tauri CLI
```bash
npm install -D @tauri-apps/cli
npx tauri --version
```

### Flask won't start
Check if port 5001 is available:
```bash
lsof -i :5001
kill -9 <PID>  # Kill existing process
```

### Window shows blank/white screen
Flask backend might not be ready:
1. Wait 5 seconds
2. Check console for errors: `npm run debug`
3. Manually test: `curl http://localhost:5001`

### Database locked error
Multiple app instances running:
```bash
pkill -f "python.*web.app"
```

## Building & Distribution

### 1. macOS (for Mac users)

Create a DMG installer:
```bash
npm run build

# Optionally code-sign (for App Store):
codesign -s - src-tauri/target/release/bundle/osx/Hidden\ Gems.app

# Create DMG:
hdiutil create -volname "Hidden Gems" -srcfolder src-tauri/target/release/bundle/osx -ov -format UDZO Hidden-Gems.dmg
```

### 2. Windows (for Windows users)

Creates MSI installer:
```bash
npm run build  # On Windows machine
# Output: Hidden Gems_1.0.0_x64.msi
```

### 3. Linux (for Linux users)

Creates AppImage (single executable):
```bash
npm run build  # On Linux machine
# Output: hidden-gems-desktop_1.0.0_amd64.AppImage
```

### Upload for distribution

1. **GitHub Releases** (free)
   - Push to GitHub
   - Create release with DMG/MSI/AppImage

2. **App Store**
   - macOS: Apple App Store
   - Windows: Microsoft Store
   - Linux: Flathub, Snap Store

3. **Self-hosted**
   - Upload to your website
   - Create download page

## Configuration

### Environment Variables

Create `.env` in app root:
```env
# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# AI/Chatbot
GROQ_API_KEY=gsk_xxxxx

# Database (auto-created if not exists)
DATABASE_URL=sqlite:///hidden_gems.db

# Flask
FLASK_ENV=production
SECRET_KEY=change-this-to-random-string
```

### Bundling secrets securely

⚠️ **Never include `.env` in distribution!**

Instead:
1. User gets app without `.env`
2. First launch prompts to enter API keys
3. Keys saved to user's config directory
4. On Windows: `%APPDATA%/Hidden Gems/`
5. On macOS: `~/Library/Application Support/Hidden Gems/`
6. On Linux: `~/.config/hidden-gems/`

## Next Steps

1. **Install Rust** if you haven't already
2. **Test dev mode**: `npm run dev`
3. **Build first release**: `npm run build`
4. **Create installer**: DMG for macOS (see above)
5. **Test on target machines** before distributing

## Support

For issues:
1. Check console: `npm run debug`
2. Verify Flask works: `curl http://localhost:5001`
3. Check port availability: `lsof -i :5001`
4. Review logs in dev console

## License & Distribution

This desktop app maintains the same license as the web version. When distributing:

1. Include LICENSE file
2. Include README with setup instructions
3. Document API key requirements (.env)
4. Provide support contact information

---

**Last updated**: February 2026
**Version**: 1.0.0
