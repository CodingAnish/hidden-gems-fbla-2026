# Hidden Gems - Business Discovery Platform 🏪

**A full-featured business discovery web application built with Flask for FBLA 2026**

A local business discovery web app that helps people find small businesses in Richmond, VA, read reviews, save favorites, and explore trending nearby businesses.

## ✨ Features

- ✅ **User Authentication** - Registration, email verification, secure password reset
- ✅ **Business Directory** - Browse, search, and filter businesses by category (Food, Retail, Services, Entertainment, Health)
- ✅ **Community Reviews** - Submit detailed reviews (10-500 characters) with 1-5 star ratings
- ✅ **Smart Validation** - Real-time validation alerts displayed at page bottom (always visible!)
- ✅ **Favorites System** - Save and manage favorite businesses with persistent storage
- ✅ **AI Chatbot** - Get personalized business recommendations via Claude AI (with rule-based fallback)
- ✅ **Interactive Map** - View businesses on Google Map with location-based filtering
- ✅ **Trending & Recommendations** - Discover popular and AI-recommended businesses
- ✅ **Responsive UI** - Mobile-friendly design for all screen sizes
- ✅ **CAPTCHA Protection** - Math-based verification to prevent spam reviews

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed
- pip (Python package manager)
- Virtual environment (highly recommended)

### Installation

1. **Clone and setup virtual environment**
   ```bash
   git clone https://github.com/[YOUR-USERNAME]/hidden-gems-fbla-2026.git
   cd hidden-gems-fbla-2026-main
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # Mac/Linux
   # or: venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application**
   ```bash
   python3 -m web.app
   ```

4. **Open in browser**
   ```
   http://localhost:5001
   ```

## 📁 Project Structure

```
hidden-gems-fbla-2026-main/
│
├── src/                          # Core business logic and database
│   ├── database/
│   │   ├── db.py                 # SQLite initialization & schema
│   │   ├── queries.py            # All database query functions
│   │   └── seed.py               # Sample data (167 businesses)
│   │
│   ├── logic/
│   │   ├── auth.py               # Password hashing & user validation
│   │   ├── chatbot.py            # AI recommendations & conversations
│   │   ├── email_sender.py       # Email delivery (SMTP)
│   │   ├── geocoding.py          # Google Maps integration
│   │   ├── yelp_api.py           # Yelp business data (optional)
│   │   └── verifier.py           # Email verification logic
│   │
│   └── __init__.py
│
├── web/                          # Flask web application
│   ├── app.py                    # Main Flask app with all routes
│   ├── static/                   # Frontend assets
│   │   ├── style.css             # Global styles
│   │   ├── features.css          # Feature-specific styles (validation alerts, reviews)
│   │   ├── chat.css              # Chatbot styles
│   │   ├── chatbot.css           # Additional chatbot styles
│   │   ├── features.js           # Reviews, favorites, validation logic
│   │   ├── chat.js               # Chatbot interface
│   │   ├── chatbot.js            # Chatbot functionality
│   │   └── manifest.json         # Progressive Web App config
│   │
│   └── templates/                # Jinja2 HTML templates
│       ├── base.html             # Base layout (navbar, footer)
│       ├── home.html             # Landing page
│       ├── directory.html        # Business directory with filters
│       ├── business.html         # Business details & review form
│       ├── map.html              # Interactive map (Google Maps)
│       ├── trending.html         # Trending businesses
│       ├── recommendations.html  # AI recommendations
│       ├── favorites.html        # Saved businesses
│       ├── profile.html          # User profile & stats
│       ├── settings.html         # User preferences
│       ├── help.html             # Help & FAQ
│       ├── login.html            # Login form
│       ├── register.html         # Registration form
│       ├── verify.html           # Email verification
│       ├── forgot-password.html  # Password reset request
│       ├── reset-password.html   # Password reset form
│       └── components/           # Reusable UI components
│           ├── review_modal.html # Review submission modal
│           ├── filters_section.html
│           ├── deals_section.html
│           └── help_menu.html
│
├── docs/                         # Comprehensive documentation
│   ├── ARCHITECTURE.md           # System design overview
│   ├── DATABASE.md               # Database schema & design
│   ├── QUICK_REFERENCE.md        # Setup quick guide
│   ├── CHATBOT_SETUP.md          # LLM integration guide
│   ├── GROQ_CHATBOT_SETUP.md     # Groq-specific setup
│   ├── EMAIL_SETUP.md            # Email configuration guide
│   └── YELP_SETUP.md             # Yelp API configuration
│
├── config.example.py             # Template for configuration
├── requirements.txt              # Python dependencies
├── render.yaml                   # Render deployment config
├── .gitignore                    # Git exclusions
└── README.md                     # This file
```

## 🔑 Key Features Explained

### Validation Alerts System
- Errors appear at **bottom center** of page (always visible!)
- Real-time field validation with character counters
- 10-500 character minimum/maximum for reviews
- CAPTCHA verification (math-based questions)
- Auto-dismisses after 10 seconds or click close button

### Review Submission
- Two methods: Modal popup (trending/recommendations) + Form (business details)
- Instant client-side validation before submission
- Server-side validation enforcement
- CAPTCHA spam protection
- Character counter: Shows "X / 500 characters" in real-time

### Database
- SQLite for local persistent storage
- 8 main tables: users, businesses, reviews, favorites, deals, verification_codes, preferences, businesses_attributes
- 167 sample businesses pre-loaded
- Automatic schema creation on first run

### AI Chatbot
- Claude integration via Groq API (free)
- Fallback to Hugging Face API
- Rule-based responses if no API available
- Conversation history management
- Rate limiting: 20 messages per session

## ⚙️ Configuration

### Environment Variables (.env)

Create a `.env` file in project root:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=generate-random-string-with-secrets.token_urlsafe()
PORT=5001

# Email Configuration (optional - for verification & password reset)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
SENDER_EMAIL=noreply@hidden-gems.io

# AI Chatbot (optional - for recommendations)
GROQ_API_KEY=your-groq-free-api-key
HUGGING_FACE_API_KEY=your-huggingface-api-key

# Maps (optional - for interactive map feature)
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Yelp (optional - for business data)
YELP_API_KEY=your-yelp-api-key
```

> ⚠️ **Important**: Never commit `.env` to Git! Already in `.gitignore`

### Generate SECRET_KEY

```python
from secrets import token_urlsafe
print(token_urlsafe(32))
```

## 🌐 Deployment to PythonAnywhere (Free + Email Support)

PythonAnywhere supports SMTP email and is perfect for this Flask app.

### Step-by-Step:

1. **Sign Up** - https://www.pythonanywhere.com (free account: 512 MB storage)

2. **Upload Code**
   ```bash
   # In PythonAnywhere Bash console:
   cd /home/yourusername
   git clone https://github.com/[YOUR-USERNAME]/hidden-gems-fbla-2026.git
   ```

3. **Create Virtual Environment**
   ```bash
   cd hidden-gems-fbla-2026-main
   mkvirtualenv --python=/usr/bin/python3.10 hidden-gems
   pip install -r requirements.txt
   ```

4. **Create Web App**
   - Go to **Web** tab → **Add a new web app**
   - Choose **Manual configuration** → **Python 3.10**

5. **Configure WSGI File**
   Edit the WSGI config file shown with:
   ```python
   import sys
   import os
   
   path = '/home/yourusername/hidden-gems-fbla-2026-main'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   os.chdir(path)
   from web.app import app as application
   ```

6. **Set Environment Variables**
   - In Web tab → **Environment variables**:
   ```
   FLASK_DEBUG=false
   PORT=5001
   SECRET_KEY=[your-generated-key]
   ```

7. **Reload Web App**
   - Click  **Reload** 
   - Your site: `yourusername.pythonanywhere.com`

## 📝 Common Routes

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Home page (featured & trending) |
| GET | `/directory` | Business directory with search/filter |
| GET | `/business/<id>` | Business details & reviews |
| GET | `/map` | Interactive map view |
| GET | `/trending` | Trending businesses |
| GET | `/recommendations` | AI recommendations |
| GET | `/favorites` | Saved businesses |
| POST | `/register` | Create account |
| POST | `/login` | User authentication |
| GET | `/logout` | End session |
| POST | `/business/<id>/review` | Submit review |
| POST | `/submit-review` | Submit review (JSON) |
| POST | `/get-captcha` | Get CAPTCHA question |

## 🧪 Testing

### Manual Testing
1. Register new account
2. Verify email (use code shown in app or check email)
3. Browse business directory
4. Try viewing business details
5. Submit review with invalid input → see validation alert at bottom!
6. Submit valid review (10+ chars, rating, CAPTCHA answer)
7. Check favorites system
8. Try chatbot (if API configured)

### Test Accounts (pre-populated)
- Email: test@example.com
- Email: demo@example.com
- (Check database seed for more)

## 🔒 Security Considerations

✅ **Implemented:**
- SHA-256 password hashing with salt
- Parameterized database queries (prevents SQL injection)
- Email verification before account activation
- Session-based authentication
- Password reset via email tokens (1-hour expiry)
- CAPTCHA on reviews
- CSRF protection via Flask sessions

⚠️ **For Production:**
- Generate new `SECRET_KEY` (don't use default!)
- Use HTTPS/TLS encryption
- Consider bcrypt instead of SHA-256 for passwords
- Implement rate limiting on API endpoints
- Configure CORS for trusted domains only
- Use environment-specific configs
- Regularly update dependencies

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 5001
lsof -i :5001
kill -9 [PID]

# Or use different port
PORT=5002 python3 -m web.app
```

### Database Errors
```bash
# Reseed database
rm hidden_gems.db
python3 -m web.app  # Recreates on startup
```

### Email Not Sending
1. Check `.env` credentials
2. For Gmail: Use App Passwords (not regular password)
3. Allow less secure apps if needed
4. Check ISP doesn't block port 587

### JavaScript/Validation Alerts Not Working
1. Clear browser cache (Cmd+Shift+R or Ctrl+Shift+R)
2. Check browser console (F12) for errors
3. Verify CSS & JS files load in Network tab
4. Try different browser to isolate issue

###  Reviews Submission Failing
- Need at least 10 characters in review text
- Need 1-5 star rating selected
- Need to answer CAPTCHA question with number
- Check validation alert at bottom of page for specific error

## 📚 Documentation

- [Quick Reference](docs/QUICK_REFERENCE.md) - Fast setup guide
- [Database Design](docs/DATABASE.md) - Schema & relationships
- [System Architecture](docs/ARCHITECTURE.md) - Component overview
- [Chatbot Setup](docs/CHATBOT_SETUP.md) - LLM configuration
- [Email Setup](docs/EMAIL_SETUP.md) - SMTP configuration
- [Google Maps Setup](GOOGLE_MAPS_SETUP.md) - Map integration

## 📋 File Naming Standards

- **Python modules**: `naming_like_this.py` (snake_case)
- **Database tables**: `plural_names` (users, businesses, reviews)
- **Database columns**: `snake_case_names`
- **HTML templates**: `noun.html` (business.html, home.html)
- **CSS files**: `feature-name.css` (features.css, validation-alerts.css)
- **JavaScript files**: `feature-name.js` (features.js, chat.js)
- **Folders**: `lowercase_plural` (src, web, docs, static, templates)

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m "Add amazing feature"`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is created for FBLA 2026 competition.

---

**Built with ❤️ for FBLA 2026**
