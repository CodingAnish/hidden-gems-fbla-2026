# Hidden Gems

Hidden Gems is a local business discovery web app for Richmond, VA. It helps people find small businesses, read reviews, save favorites, and explore what is trending nearby.

## Overview

The project is built around a Flask web app backed by a local SQLite database. The core logic lives in the `src` package (database, auth, integrations) and is shared across the app. An optional AI chatbot can be enabled with free API keys, but the app also works without them.

## Features

- User accounts with email verification
- Business directory with search and filters
- Reviews and ratings
- Favorites list
- Trending and recommendations pages
- AI chatbot with a rule-based fallback
- Mobile-friendly, responsive UI

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Install

1. Clone the repo and move into it.
2. (Optional) Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Copy the config template:
```bash
cp config.example.py config.py
```
5. Initialize the database:
```bash
python -m src.database.seed
```
6. Start the web app:
```bash
python -m web.app
```
Then open http://127.0.0.1:5000.

## Configuration

Most settings live in `config.py`. API keys are optional but unlock extra features.

- Yelp data: see [docs/YELP_SETUP.md](docs/YELP_SETUP.md)
- Email verification: see [docs/EMAIL_SETUP.md](docs/EMAIL_SETUP.md)
- Chatbot setup: see [docs/CHATBOT_SETUP.md](docs/CHATBOT_SETUP.md)
- Groq chatbot details: see [docs/GROQ_CHATBOT_SETUP.md](docs/GROQ_CHATBOT_SETUP.md)

If no API keys are configured, the chatbot falls back to rule-based responses and the app uses sample business data.

### Optional .env

If you prefer environment variables, create a `.env` file and load it in your app entry point. The setup guides show both patterns.

## Database

The database file is created as `hidden_gems.db` in the project root. The seed script loads sample businesses and sets up the schema. Details are in [docs/DATABASE.md](docs/DATABASE.md).

## Common Routes

```
GET  /               Home
GET  /directory      Business directory
GET  /business/<id>  Business detail
GET  /favorites      Favorites (login required)
GET  /recommendations Recommendations (login required)
GET/POST /register
GET/POST /login
GET      /logout
GET/POST /verify
GET/POST /forgot-password
```

## Project Structure

```
hidden-gems/
├── src/                  # Shared logic (database, auth, APIs)
├── web/                  # Flask app, templates, static assets
├── docs/                 # Documentation
├── config.example.py     # Config template
├── requirements.txt      # Python dependencies
└── README.md
```

## Security Notes

- Passwords are hashed and salted.
- Login requires verified email.
- All database queries are parameterized.

## Deployment

The Flask app can be deployed on any host that supports Python and WSGI (Railway, Render, PythonAnywhere, and similar).

## Troubleshooting

- Server will not start: stop old processes with `pkill -f "python.*web.app"`, then restart.
- Missing data: run `python -m src.database.seed` again to re-seed sample data.
- Email verification not sending: check `config.py` and [docs/EMAIL_SETUP.md](docs/EMAIL_SETUP.md).

## Support

If you are setting up the project for the first time, start with [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md).
