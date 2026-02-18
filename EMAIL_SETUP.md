# Send real verification emails (Gmail)

To have Hidden Gems email the 6-digit code to users instead of showing it on screen:

## 1. Create a Gmail App Password

1. Go to [Google Account → Security](https://myaccount.google.com/security).
2. Turn on **2-Step Verification** if it’s not already on.
3. Open [App passwords](https://myaccount.google.com/apppasswords).
4. Choose **Mail** and **Windows Computer** (or Other), then **Generate**.
5. Copy the **16-character password** (no spaces).

## 2. Edit `config.py`

In the project folder, open **config.py** and set:

- **SMTP_USER** = your Gmail address (e.g. `"you@gmail.com"`)
- **SMTP_PASSWORD** = the 16-character App Password from step 1 (in quotes)
- **FROM_EMAIL** = same as SMTP_USER

Example:

```python
SMTP_USER = "myemail@gmail.com"
SMTP_PASSWORD = "abcd efgh ijkl mnop"   # your App Password
FROM_EMAIL = "myemail@gmail.com"
```

Save the file.

## 3. Run the app

Start Hidden Gems with `python main.py`. When someone registers or needs to verify, the code will be sent to their email and the app will say “We've sent a verification code to …”.

---

**Other email providers:** Use their SMTP server and port in `config.py` (e.g. Outlook: `smtp.office365.com`, port 587). The same `SMTP_USER` / `SMTP_PASSWORD` / `FROM_EMAIL` idea applies.
