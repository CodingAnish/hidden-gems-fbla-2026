# Groq Chatbot Setup

This guide focuses on using Groq as the primary AI provider for the Hidden Gems chatbot.

## 1. Create a Groq API Key

1. Go to https://console.groq.com and create an account.
2. Open the **API Keys** page and create a new key.
3. Copy the key (it starts with `gsk_`).

## 2. Save the Key

You can store the key in either `.env` or `config.py`.

### Option A: `.env`

Create a `.env` file in the project root:

```
GROQ_API_KEY=gsk_your_key_here
```

Make sure `.env` is listed in `.gitignore`.

### Option B: `config.py`

Copy the template and paste the key:

```bash
cp config.example.py config.py
```

```python
GROQ_API_KEY = "gsk_your_key_here"
```

## 3. Run and Test

1. Start the app:
   ```bash
   python -m web.app
   ```
2. Open http://localhost:5000 and log in.
3. Click the chat button and send a prompt like “find restaurants”.

If you receive a response, the integration is working.

## How It Works

- The frontend sends messages to `/api/chat`.
- The backend builds a business-aware prompt and calls Groq.
- If Groq fails or no key is set, the chatbot falls back to rule-based replies.

## Troubleshooting

- No response: check that the Flask app is running and you are logged in.
- API error: confirm the key starts with `gsk_` and has no extra spaces.
- Slow responses: Groq should be fast; check your connection or rate limits.

## Optional: Change the Model

In `src/logic/chatbot.py`, you can change the model name used in the Groq request payload.

## Resources

- Groq Console: https://console.groq.com
- Groq API Docs: https://console.groq.com/docs
