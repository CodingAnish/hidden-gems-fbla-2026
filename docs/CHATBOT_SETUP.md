# Chatbot Setup

Hidden Gems supports three chatbot modes. You can use one, mix them, or leave all API keys empty and still get responses.

## Option 1: Groq API (fast, free tier)

Groq is the quickest option and works well for live demos.

**Setup:**
1. Create an account at https://console.groq.com.
2. Create an API key.
3. Add it to `config.py`:
   ```python
   GROQ_API_KEY = "gsk_your_key_here"
   ```
4. Restart the Flask app.

## Option 2: Hugging Face (backup)

Hugging Face is a good backup provider. The first response can be slow while the model wakes up.

**Setup:**
1. Create an account at https://huggingface.co.
2. Generate a read token.
3. Add it to `config.py`:
   ```python
   HUGGINGFACE_API_KEY = "hf_your_key_here"
   ```
4. Restart the Flask app.

## Option 3: Rule-based (no API required)

If no keys are set, the chatbot uses a built-in rule-based fallback. It is instant and works offline.

## Fallback Order

The chatbot tries providers in this order:

1. Groq (if configured)
2. Hugging Face (if configured and Groq fails)
3. Rule-based fallback

## Quick Test

1. Start the app: `python -m web.app`
2. Open http://127.0.0.1:5000
3. Click the chat button and send: “find restaurants”

If you see a response, the chatbot is working.

## Common Issues

- No response: confirm the Flask app is running and refresh the page.
- Authentication errors: log in first (chat requires a session).
- API errors: verify the key prefix and remove extra spaces in `config.py`.
