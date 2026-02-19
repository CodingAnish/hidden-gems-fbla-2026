# Hidden Gems Quick Reference

This page is a short guide for running the web app and testing the core flows.

## Quick Start

1. Start the server:
   ```bash
   python -m web.app
   ```
2. Open the app:
   ```
   http://localhost:5000
   ```

## Create a Test Account

Use any username/email you like. Example:

```
Username: testuser
Email:    test@example.com
Password: TestPass123!
```

You will see a 6-digit verification code after registering. Enter it to complete the login flow.

## Key Routes

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

## Common Checks

- Register and verify email
- Browse the directory and open a business page
- Add a favorite and confirm it appears under Favorites
- Write a review and confirm it appears on the business page
- Open the chatbot and try a few prompts

## Troubleshooting

- Server will not start: stop old processes with `pkill -f "python.*web.app"`, then restart.
- Verification issues: confirm the code is copied exactly as shown.
- API errors: double-check keys in `config.py` or `.env`.

## Related Docs

- Chatbot setup: [docs/CHATBOT_SETUP.md](docs/CHATBOT_SETUP.md)
- Groq details: [docs/GROQ_CHATBOT_SETUP.md](docs/GROQ_CHATBOT_SETUP.md)
- Email setup: [docs/EMAIL_SETUP.md](docs/EMAIL_SETUP.md)
- Yelp setup: [docs/YELP_SETUP.md](docs/YELP_SETUP.md)
