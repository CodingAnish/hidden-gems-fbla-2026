# Hidden Gems - Local Business Discovery Platform

A modern web application for discovering and reviewing local businesses in Richmond, Virginia. Built with Flask for FBLA 2026.

## Overview

Hidden Gems helps residents discover small, independent businesses through browsing, searching, reviews, and AI-powered recommendations. The platform combines community reviews, interactive maps, and intelligent chatbot assistance to connect people with local gems they might otherwise miss.

## Key Features

- **User Authentication** - Secure registration, email verification, and password reset functionality
- **Business Directory** - Browse and filter businesses by category, ratings, and reviews
- **Community Reviews** - Submit detailed reviews with 1-5 star ratings and spam protection via CAPTCHA
- **Favorites System** - Save and manage your favorite businesses for quick access
- **AI Chatbot** - Get personalized business recommendations powered by Groq's Llama 3 API
- **Interactive Map** - View business locations and explore neighborhoods with Google Maps integration
- **Trending Section** - Discover what other users are reviewing and enjoying
- **Responsive Design** - Fully mobile-friendly interface for on-the-go business hunting
- **Real-time Validation** - Intuitive validation alerts for forms and user input

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CodingAnish/hidden-gems-fbla-2026.git
   cd hidden-gems-fbla-2026-main
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or: venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (optional - app works without them)
   ```

5. **Run the application**
   ```bash
   python3 -m web.app
   ```

6. **Access the app**
   - Open http://localhost:5001 in your browser

## Project Structure

```
hidden-gems-fbla-2026-main/
├── config/                       # Configuration files and templates
│   ├── config.py                 # Live configuration (local development)
│   └── config.example.py         # Configuration template
│
├── src/                          # Core application logic
│   ├── database/
│   │   ├── db.py                 # SQLite initialization and schema
│   │   ├── queries.py            # All database query functions
│   │   └── seed.py               # Sample data (167 businesses, 5 categories)
│   │
│   ├── logic/
│   │   ├── auth.py               # User authentication and password hashing
│   │   ├── chatbot.py            # AI chatbot with Groq API integration
│   │   ├── email_sender.py       # SendGrid email delivery
│   │   ├── geocoding.py          # Google Maps geocoding
│   │   ├── yelp_api.py           # Optional Yelp API integration
│   │   └── verifier.py           # Email verification logic
│   │
│   └── verification/             # Email verification module
│       └── verifier.py
│
├── web/                          # Flask web application
│   ├── app.py                    # Main Flask app with all routes
│   ├── static/                   # Frontend assets
│   │   ├── style.css             # Global styling
│   │   ├── features.css          # Feature-specific styles
│   │   ├── chat.css              # Chatbot interface styles
│   │   ├── chatbot.css           # Additional chatbot styling
│   │   ├── features.js           # Reviews, favorites, validation
│   │   ├── chat.js               # Chat interface logic
│   │   ├── chatbot.js            # Chatbot functionality
│   │   └── manifest.json         # PWA configuration
│   │
│   └── templates/                # Jinja2 HTML templates
│       ├── base.html             # Base layout template
│       ├── home.html             # Landing page
│       ├── directory.html        # Business directory and search
│       ├── business.html         # Business details and reviews
│       ├── map.html              # Interactive map
│       ├── trending.html         # Trending businesses
│       ├── recommendations.html  # AI recommendations
│       ├── favorites.html        # Saved businesses
│       ├── profile.html          # User profile
│       ├── settings.html         # User settings
│       ├── help.html             # Help and FAQ
│       ├── login.html            # Login form
│       ├── register.html         # Registration form
│       ├── verify.html           # Email verification
│       ├── forgot-password.html  # Password reset
│       ├── reset-password.html   # New password form
│       └── components/           # Reusable UI components
│           ├── review_modal.html
│           ├── filters_section.html
│           ├── deals_section.html
│           └── help_menu.html
│
├── docs/                         # Comprehensive documentation
│   ├── ARCHITECTURE.md           # System design and overview
│   ├── DATABASE.md               # Database schema and design
│   ├── QUICK_REFERENCE.md        # Quick setup guide
│   ├── DEPLOYMENT.md             # Render deployment guide
│   ├── CHATBOT_SETUP.md          # AI chatbot configuration
│   ├── GROQ_CHATBOT_SETUP.md     # Groq-specific setup
│   ├── EMAIL_SETUP.md            # Email configuration
│   ├── YELP_SETUP.md             # Yelp API setup
│   └── GOOGLE_MAPS_SETUP.md      # Google Maps integration
│
├── scripts/                      # Utility scripts
│   ├── geocode_businesses.py     # Batch geocoding utility
│   └── inspect_map.py            # Map inspection tool
│
├── tests/                        # Test files
│   ├── test_geocoding_integration.py
│   ├── test_map_comprehensive.py
│   └── test_map_load.py
│
├── requirements.txt              # Python dependencies
├── render.yaml                   # Render platform configuration
├── .env.example                  # Environment variables template
├── .gitignore                    # Git exclusion rules
└── README.md                     # This file
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask 3.1.3 |
| **Database** | SQLite |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Maps** | Google Maps JavaScript API |
| **Email** | SendGrid API (100 free emails/day) |
| **AI Chatbot** | Groq API (free, ultra-fast LLM) |
| **Deployment** | Render.com (free tier) |
| **APIs** | Yelp Business, Google Geocoding |

## Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
PORT=5001

# Email (SendGrid) - Optional
SENDGRID_API_KEY=SG.your-api-key
FROM_EMAIL=your-email@domain.com

# AI Chatbot (Groq) - Optional but recommended
GROQ_API_KEY=gsk_your-groq-api-key

# Google Maps - Optional
GOOGLE_MAPS_API_KEY=your-google-maps-key

# Yelp API - Optional
YELP_API_KEY=your-yelp-api-key

# HuggingFace - Optional
HUGGINGFACE_API_KEY=your-hf-api-key
```

**Note:** The application works without these optional API keys - everything except email and AI chatbot will function normally.

### Generating SECRET_KEY

```python
from secrets import token_urlsafe
print(token_urlsafe(32))
```

## Deployment

### Deploy to Render (Recommended - Free)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Select Python 3.10
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python -m web.app`
6. Add environment variables in Render dashboard
7. Deploy

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## Features Explained

### AI Chatbot

The app uses Groq's Llama 3.1 8B Instant model for ultra-fast business recommendations. The chatbot:
- Provides personalized suggestions based on user preferences
- Maintains conversation history for context
- Falls back to rule-based responses if API unavailable
- Optimized for sub-second response times

**API Priority**: Cohere → Groq → HuggingFace → Rule-based

### Review System

- Minimum 10 characters, maximum 500 characters
- 1-5 star rating required
- CAPTCHA math question for spam prevention
- Real-time client-side validation
- Server-side validation enforcement

### Database

- **Engine**: SQLite3
- **Tables**: users, businesses, reviews, favorites, deals, verification_codes, preferences, businesses_attributes
- **Pre-loaded**: 167 sample businesses across 5 categories
- **Schema**: Auto-created on first run

## Common Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page with featured businesses |
| `/directory` | GET | Browse and search all businesses |
| `/business/<id>` | GET | View business details and reviews |
| `/map` | GET | Interactive map view |
| `/trending` | GET | Trending businesses |
| `/recommendations` | GET | AI recommendations |
| `/favorites` | GET | Your saved businesses |
| `/register` | POST | Create new account |
| `/login` | POST | User authentication |
| `/logout` | GET | End session |
| `/business/<id>/review` | POST | Submit review |

## Security

**Implemented Protections:**
- SHA-256 password hashing with salt
- Parameterized SQL queries (SQL injection prevention)
- Email verification before account activation
- Session-based authentication
- Password reset tokens with expiration
- CAPTCHA on review submissions
- CSRF protection via Flask sessions

**Production Recommendations:**
- Generate unique `SECRET_KEY` for your deployment
- Use HTTPS/TLS for all connections
- Consider bcrypt for password hashing
- Implement rate limiting on API endpoints
- Configure CORS policies
- Keep dependencies updated

## Troubleshooting

### Port Already in Use
```bash
lsof -i :5001  # Find process
kill -9 [PID]  # Kill it
```

### Database Errors
```bash
rm hidden_gems.db
python3 -m web.app  # Recreates on startup
```

### Email Not Sending
- Verify `SENDGRID_API_KEY` in environment variables
- Check that sender email is verified in SendGrid dashboard
- App will show verification code on-screen if email fails

### Chatbot Not Responding
- Check `GROQ_API_KEY` is set correctly
- Verify API key is active on groq.com
- Check internet connectivity
- Review will suggest businesses even without AI

### JavaScript/Validation Alerts Not Working
1. Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+R)
2. Open Developer Console (F12) to check for errors
3. Verify CSS and JS files load in Network tab
4. Try different browser to isolate issue

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - System design and component details
- [Database Design](docs/DATABASE.md) - Schema, relationships, and queries
- [Quick Reference](docs/QUICK_REFERENCE.md) - Fast setup checklist
- [Deployment Guide](docs/DEPLOYMENT.md) - Render deployment steps
- [Chatbot Setup](docs/CHATBOT_SETUP.md) - Complete chatbot configuration
- [Email Configuration](docs/EMAIL_SETUP.md) - SendGrid setup guide
- [Google Maps Integration](docs/GOOGLE_MAPS_SETUP.md) - Maps configuration

## Testing

### Manual Testing Workflow
1. Register a new account
2. Verify email (code shown in app or check SendGrid)
3. Browse businesses and search
4. View business details and existing reviews
5. Submit a review (test validation with short text first)
6. Try the chatbot for recommendations
7. Test favorites - save and retrieve businesses
8. Check profile and settings pages

### Sample Data
Pre-loaded database includes:
- 5 categories: Food, Retail, Services, Entertainment, Health
- 167 sample businesses across Richmond, VA
- Multi-word search compatible
- Geographic coordinates for map display

## API Keys & Services

**Free Tiers Used:**
- **Groq**: Free tier with no credit card required
- **SendGrid**: 100 emails/day free forever
- **Google Maps**: Free tier
- **HuggingFace**: Free inference API

## Performance Optimizations

- Llama 3.1 8B Instant model for sub-second responses
- Minimal context window for fast generation
- Client-side form validation before server processing
- SQLite indexes on frequently queried columns
- Static file minification ready

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m "Add amazing feature"`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Style

- **Python**: PEP 8 (snake_case for functions/variables, PascalCase for classes)
- **HTML**: Indented 4 spaces, semantic HTML5
- **CSS**: Mobile-first responsive design
- **JavaScript**: Vanilla JS, camelCase,descriptive naming

## License

Created for FBLA 2026 competition.

## Support

For issues, questions, or suggestions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review documentation in `/docs` folder
3. Open a GitHub issue with detailed description

---

Last Updated: February 2026
