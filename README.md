# 🌟 Hidden Gems - Richmond Business Discovery Platform

**FBLA 2026 Project**  
A modern, full-stack application for discovering and supporting local businesses in Richmond, VA.

## 🎯 Overview

Hidden Gems is a comprehensive business discovery platform featuring both a **Flask web application** and a **Python desktop application**, complete with AI-powered chatbot assistance. The platform helps users discover local businesses, read reviews, save favorites, and explore trending spots in Richmond.

## ✨ Features

### Web Application (Flask)
- 🔐 **User Authentication** - Secure login/registration with email verification
- 🏢 **Business Directory** - Browse and search Richmond businesses
- ⭐ **Reviews & Ratings** - Read and write business reviews
- ❤️ **Favorites** - Save and manage favorite businesses
- 🔥 **Trending** - Discover popular businesses
- 🎯 **Personalized Recommendations** - AI-powered business suggestions
- 💬 **AI Chatbot** - Interactive assistant using Groq/Hugging Face APIs
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

### Desktop Application (Python/Tkinter)
- 🎨 **Modern UI** - Mobile-app-style interface with premium design
- 📊 **Dashboard** - View stats, featured businesses, and quick actions
- 🔍 **Browse** - Search and filter businesses by category
- ❤️ **Favorites Management** - Track your favorite spots
- 👤 **Account Settings** - Update username and password
- 🔔 **Toast Notifications** - Interactive feedback system

### AI Chatbot Features
- 💬 Conversational interface with Groq API (Llama 3.3 70B)
- 🎯 Intent recognition (search, recommendations, deals, etc.)
- 📚 Context-aware responses using business data
- 🚀 Quick action buttons for common tasks
- 🔄 Multi-API support with automatic fallback
- 🤖 Rule-based backup when APIs unavailable

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd FBLA2026
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up configuration**
```bash
# Copy the example config file
cp config.example.py config.py

# Edit config.py and add your API keys (optional but recommended)
```

4. **Initialize the database**
```bash
python -m src.database.seed
```

5. **Run the web application**
```bash
python -m web.app
```
Then open http://127.0.0.1:5000 in your browser.

6. **Run the desktop application**
```bash
python -m src.main
```

## 🔑 API Keys (Optional)

The application works without API keys but has enhanced features when configured:

### Yelp API (Business Data)
- Free tier available
- Sign up: https://www.yelp.com/developers/v3/manage_app
- Add to `config.py`: `YELP_API_KEY = "your-key"`

### Groq API (AI Chatbot - Recommended)
- 100% free, no credit card required
- Fast inference with Llama 3.3 70B model
- Sign up: https://console.groq.com/keys
- Add to `config.py`: `GROQ_API_KEY = "your-key"`

### Hugging Face API (Backup Chatbot)
- Free tier: 1000 requests/day
- Sign up: https://huggingface.co/settings/tokens
- Add to `config.py`: `HUGGINGFACE_API_KEY = "your-key"`

### Email (Verification Codes)
- Gmail app password recommended
- Guide: https://myaccount.google.com/apppasswords
- Add credentials to `config.py`

**Note:** The chatbot automatically falls back to rule-based responses if no API keys are configured.

## 📁 Project Structure

```
FBLA2026/
├── src/                          # Desktop application
│   ├── ui/                       # UI components and design system
│   │   ├── components/          # Reusable UI components
│   │   ├── design_system.py     # Colors, fonts, spacing
│   │   ├── login_window.py      # Authentication UI
│   │   ├── main_menu.py         # Main dashboard
│   │   └── account_settings.py  # Settings window
│   ├── database/                 # Database layer
│   │   ├── db.py                # Connection management
│   │   ├── queries.py           # SQL queries
│   │   └── seed.py              # Database initialization
│   └── logic/                    # Business logic
│       ├── yelp_api.py          # Yelp integration
│       ├── chatbot.py           # AI chatbot logic
│       └── verification.py      # Bot detection
├── web/                          # Flask web application
│   ├── app.py                   # Main Flask app
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, images
│       ├── chat.css             # Chatbot styles
│       └── chat.js              # Chatbot frontend
├── config.py                     # Configuration (not in git)
├── config.example.py            # Configuration template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🎨 Design System

The application features a modern, mobile-app-inspired design:

- **Colors**: Teal primary (#06b6d4), soft neutrals, gradients
- **Typography**: Segoe UI with clear hierarchy
- **Components**: Rounded cards, soft shadows, hover animations
- **Layout**: Mobile-first, responsive, breathable spacing
- **Interactions**: Toast notifications, loading states, micro-animations

## 🛠️ Technologies Used

### Backend
- **Python 3** - Core language
- **Flask** - Web framework
- **SQLite** - Database
- **Yelp Fusion API** - Business data
- **Groq API** - AI chatbot (Llama 3.3)

### Frontend
- **Tkinter** - Desktop GUI
- **HTML/CSS/JavaScript** - Web interface
- **Responsive Design** - Mobile-friendly layouts

### AI/ML
- **Groq (Llama 3.3 70B)** - Primary chatbot
- **Hugging Face (Llama 3.2 3B)** - Backup chatbot
- **Rule-based Logic** - Fallback system

## 📱 Screenshots

### Web Application
- Modern dashboard with business directory
- AI chatbot with slide-out panel
- Responsive design for all devices

### Desktop Application
- Premium mobile-app-style interface
- Card-based navigation
- Interactive business browsing

## 🧪 Testing

1. **Create a test account** in the web or desktop app
2. **Browse businesses** to see the directory
3. **Try the AI chatbot** (web app, login required)
4. **Add favorites** and view them
5. **Leave reviews** and ratings
6. **Update account settings**

## 📊 Database Schema

- **users** - User accounts and authentication
- **businesses** - Business information from Yelp
- **reviews** - User reviews and ratings
- **favorites** - User's saved businesses
- **verification_logs** - Security tracking

## 🔒 Security Features

- Password hashing with SHA-256
- Email verification system
- Bot detection challenges
- Session management
- Input validation and sanitization

## 🎓 FBLA 2026 Notes

This project demonstrates:
- Full-stack development skills
- Database design and management
- API integration (Yelp, Groq, Hugging Face)
- Modern UI/UX design principles
- Secure authentication systems
- AI/ML integration
- Cross-platform development (web + desktop)

## 📝 License

This project is created for FBLA 2026 competition purposes.

## 🤝 Contributing

This is an FBLA competition project. For questions or suggestions, please contact the team.

## 📧 Support

For setup help or questions:
1. Check `CHATBOT_SETUP.md` for chatbot configuration
2. Check `EMAIL_SETUP.md` for email setup (if present)
3. Review the code comments for implementation details

## 🚀 Deployment

### Web App
The Flask app can be deployed to:
- Heroku
- Railway
- Render
- PythonAnywhere
- Any platform supporting Python/Flask

### Desktop App
The desktop app can be packaged using:
- PyInstaller
- cx_Freeze
- py2exe (Windows)
- py2app (macOS)

---

**Built with ❤️ for FBLA 2026**  
Discover Richmond's Hidden Gems! 🌟
