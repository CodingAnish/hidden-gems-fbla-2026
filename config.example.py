# Hidden Gems — Config Example
# Copy this file to config.py and add your own API keys

# ---- Email (verification codes) ----
# See EMAIL_SETUP.md. Gmail: https://myaccount.google.com/apppasswords
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "hiddengem.official26@gmail.com"  # Your Gmail address
SMTP_PASSWORD = "tozr qizo htta pmjc"  # App password from Google
FROM_EMAIL = ""  # Your Gmail address
FROM_NAME = "Hidden Gems"

# ---- Yelp (Richmond, VA businesses) ----
# Get a free API key: https://www.yelp.com/developers/v3/manage_app
# Create App, then copy API Key. Leave empty to use sample businesses only.
YELP_API_KEY = ""

# ---- FREE AI Chatbot APIs ----
# Option 1: Groq API (RECOMMENDED - Free, Fast, Best for demos)
# Get free key: https://console.groq.com/keys (no credit card needed)
GROQ_API_KEY = ""

# Option 2: Hugging Face (FREE backup - 1000 requests/day)
# Get free key: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY = ""

# Note: Chatbot will automatically fall back to rule-based mode if no API keys are set
