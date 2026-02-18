# Hidden Gems - App Sharing Guide

## Option 1: Easiest - Share Source Code (Recommended)

Share the code with others and they can run it locally:

### For Others to Use Your App:

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd hidden-gems-fbla-2026-main
   ```

2. **Install dependencies** 
   ```bash
   # Install Python dependencies
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   
   # Install Node dependencies
   npm install
   ```

3. **Run the desktop app**
   ```bash
   npm run dev
   ```

   This launches the full desktop app with Flask backend automatically.

4. **Or run just the web version**
   ```bash
   .venv/bin/python -m web.app
   # Then open browser to http://localhost:5001
   ```

---

##Option 2: Docker (Easy deployment to cloud)

Share a Docker image that anyone can run:

```dockerfile
# Create Dockerfile in root
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=web.app
CMD [".venv/bin/python", "-m", "web.app"]
```

Then others can run:
```bash
docker run -p 5001:5001 your-image-name
```

---

## Option 3: Web-Only (Easiest for most users)

Deploy Flask app to cloud services. Once live:
- Share simple link: `https://hidden-gems.example.com`
- No installation needed
- Works on any browser

### Deploy to Render (Free):
1. Push code to GitHub
2. Connect to Render.com
3. Deploy → Get live link in 2 minutes

---

## Option 4: Standalone Installers (Advanced)

Build `.dmg` (Mac), `.msi` (Windows), `.AppImage` (Linux):
```bash
npm run build
# Installers created in: src-tauri/target/release/bundle/
```

**Current limitation**: Requires adding native Python embedding or using PyInstaller to fully bundle Flask backend with the app.

---

## Recommended Setup for Sharing:

**For developers/technical users:**
- Use Option 1 (source code + `npm run dev`)
- They get full desktop app with all features

**For end-users:**
- Use Option 3 (deploy to cloud)  
- Share the live URL
- Works instantly in any browser

---

## Environment Setup for Shared Code

Include `.env.example`:
```
GROQ_API_KEY=your_key_here
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_password
SMTP_FROM_NAME=Hidden Gems
YELP_API_KEY=your_key_here
```

Users copy to `.env` and fill in their own API keys.

---

**Which method do you prefer?**
- **Option 1**: Fast, works immediately
- **Option 2**: Docker for full environment isolation
- **Option 3**: Web URL (simplest for everyone)
- **Option 4**: Installer files (most professional, but requires extra setup)
