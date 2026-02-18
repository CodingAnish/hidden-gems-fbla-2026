# Groq AI Chatbot - Quick Reference Card

## 5-Minute Setup Checklist

### Get Your API Key (3 minutes)
- [ ] Go to https://console.groq.com
- [ ] Sign up (no credit card needed)
- [ ] Click "API Keys" in sidebar
- [ ] Click "Create API Key"
- [ ] Name it "Hidden Gems Chatbot"
- [ ] Copy the key (starts with `gsk_`)

### Configure Your Key (2 minutes)
Choose ONE method:

**Method A: `.env` file (Recommended)**
```bash
# Create .env in project root
echo "GROQ_API_KEY=gsk_your_key_here" > .env
echo ".env" >> .gitignore
```

**Method B: `config.py` file**
```bash
# Copy the example
cp config.example.py config.py

# Edit config.py and add:
GROQ_API_KEY = "gsk_your_key_here"

# Add to gitignore
echo "config.py" >> .gitignore
```

## Test Your Setup

```bash
# Terminal 1: Start Flask
python -m web.app
# Should show: * Running on http://0.0.0.0:5000

# Terminal 2: Test API
curl http://localhost:5000/api/chat/welcome
# Should return JSON with welcome message
```

## Use the Chatbot

1. Open http://localhost:5000
2. **Log in** with your account
3. Look for **floating chat button** (bottom-right, teal color)
4. Click it to open chat
5. Type a message and hit Enter

## Example Messages to Test

```
"Hello"                           → Gets welcome message
"Find restaurants"                → Shows restaurant recommendations
"Show me the best rated"          → Top 3-5 businesses
"What deals are available?"       → Current promotions
"Compare [business] with [other]" → Detailed comparison
```

## Quick Actions

After each bot response, click suggested buttons instead of typing.

## Free Tier Limits

- 30 requests/minute (very generous)
- 14,400 requests/day (plenty)
- Cost: **$0.00** (100% free!)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No chat button | Make sure you're logged in |
| "Not authenticated" error | Clear cookies, log in again |
| Slow responses | Check internet (should be <1 sec) |
| API errors | Verify key in config, restart Flask |

## File Locations

```
web/
├── templates/
│   ├── chatbot.html        ← Chat widget (new)
│   └── base.html           ← Updated to include chatbot
├── static/
│   ├── chatbot.css         ← Chat styling (new)
│   └── chatbot.js          ← Chat logic (new)
└── app.py                  ← Already has /api/chat endpoints

src/logic/
└── chatbot.py              ← Groq integration (ready)

GROQ_CHATBOT_SETUP.md       ← Full setup guide (new)
```

## For FBLA Demo

**What to show judges:**
1. Click chat button
2. Send a message about finding a business
3. Show bot recommends businesses from database
4. Mention: "Using FREE Groq API - no costs!"
5. Explain: "AI-powered with < 1 second response time"

**Key talking points:**
- Free AI (Groq tier)
- Unlimited scale (14,400 daily)
- Secure (API key on backend only)
- Works on mobile
- Natural language interface

## Common Customizations

**Change chat colors (in `chatbot.css`):**
```css
.chat-button, .send-button {
  background: linear-gradient(135deg, #YOUR_COLOR_1, #YOUR_COLOR_2);
}
```

**Change bot personality (in `chatbot.py`):**
Edit `get_business_context()` function to change system prompt.

**Change quick action buttons:**
Edit `get_quick_actions()` function in `chatbot.py`.

## Next Steps

1. ✅ Add API key to config
2. ✅ Run Flask server
3. ✅ Test chat button
4. ✅ Practice demo
5. 🎉 Show judges the AI chatbot!

---

**Questions?** Check `GROQ_CHATBOT_SETUP.md` for detailed guide.

**Cost Estimate:** $0.00 + Your time = Working AI chatbot 🚀
