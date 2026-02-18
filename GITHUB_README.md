# Hidden Gems - Desktop App

A lightweight desktop application for discovering hidden gem businesses in your area. Find amazing local restaurants, shops, and services that are off the beaten path.

![Built with Tauri](https://img.shields.io/badge/Built%20with-Tauri-24C8DB?style=flat-square)
![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square)
![React](https://img.shields.io/badge/Frontend-Tauri-24C8DB?style=flat-square)

## Features

✨ **Browse Businesses** - Discover thousands of local businesses  
🔍 **Smart Search** - Find businesses by name, category, or location  
⭐ **Ratings & Reviews** - See community feedback  
❤️ **Favorites** - Save your favorite discoveries  
💬 **AI Chatbot** - Get personalized recommendations  
📱 **Desktop App** - Native cross-platform application  

## Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 16+**
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/hidden-gems-fbla-2026.git
   cd hidden-gems-fbla-2026-main
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install Node dependencies**
   ```bash
   npm install
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   - `GROQ_API_KEY` - Get from [console.groq.com](https://console.groq.com)
   - `YELP_API_KEY` - Get from [yelp.com/developers](https://www.yelp.com/developers)
   - `SMTP_*` - Email settings for password resets

### Run the App

**Desktop version (recommended):**
```bash
npm run dev
```
This launches the full desktop application with Flask backend automatically.

**Web-only version:**
```bash
.venv/bin/python -m web.app
```
Then open http://localhost:5001 in your browser.

## Project Structure

```
hidden-gems-fbla-2026/
├── web/                    # Flask web app
│   ├── app.py             # Main Flask application
│   ├── templates/         # HTML templates
│   └── static/            # CSS, JavaScript, assets
├── src/                   # Python backend logic
│   ├── database/          # Database and seed data
│   ├── logic/             # Business logic (chatbot, auth, etc)
│   └── ui/                # Desktop UI components
├── src-tauri/             # Tauri desktop framework
│   └── src/main.rs        # Rust entry point
├── java-app/              # Optional Java backend
├── requirements.txt       # Python dependencies
└── package.json          # Node dependencies
```

## Development

### Available Commands

```bash
# Development
npm run dev              # Run desktop app in dev mode
npm run build            # Build desktop installers
.venv/bin/python -m web.app  # Run web server only

# Code Quality
npm run lint             # Lint JavaScript code
```

### Database

The app uses SQLite with automatic seeding. On first run, it creates:
- Sample businesses
- Demo users
- Test data

To reset:
```bash
rm hidden_gems.db
```

## Deployment

### Option 1: Local/Development (Current Setup)
Perfect for sharing with developers. Just clone and run `npm run dev`.

### Option 2: Docker
```bash
docker build -t hidden-gems .
docker run -p 5001:5001 hidden-gems
```

### Option 3: Web Deployment
Deploy Flask backend to Render, Railway, or Heroku for a live URL.

## Configuration

### Environment Variables

Create `.env` file (copy from `.env.example`):

```env
# AI/Chatbot
GROQ_API_KEY=gsk_your_key_here

# Yelp API
YELP_API_KEY=your_key_here

# Email (Password Resets)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_NAME=Hidden Gems

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

## System Requirements

### macOS
- macOS 10.13 or later
- ~200MB disk space (with dependencies)

### Windows
- Windows 7 or later
- ~200MB disk space

### Linux
- Ubuntu 18.04+ or equivalent
- ~200MB disk space

## Troubleshooting

### Port 5001 already in use
```bash
# macOS/Linux
lsof -i :5001 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

### Python module not found
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Tauri build errors
Clean and rebuild:
```bash
rm -rf src-tauri/target src-tauri/Cargo.lock
npm run build
```

## Tech Stack

- **Frontend**: HTML/CSS/JavaScript (Jinja2 templates)
- **Backend**: Flask (Python)
- **Desktop**: Tauri + Rust
- **Database**: SQLite
- **AI**: Groq API
- **Business Data**: Yelp API
- **UI Framework**: Custom CSS (Tailwind-inspired)

## License

This project is part of the FBLA 2026 competition.

## Support

- 📖 See [SHARING_GUIDE.md](SHARING_GUIDE.md) for deployment options
- 🐛 Report issues on GitHub
- 💬 Check existing documentation in `/docs`

## Credits

Built by Hidden Gems Team for FBLA 2026

---

**Ready to share?** Push to GitHub and share the repository link with your team!

See [SHARING_GUIDE.md](SHARING_GUIDE.md) for more options.
