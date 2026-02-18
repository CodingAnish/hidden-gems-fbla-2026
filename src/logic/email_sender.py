"""
Send verification emails via SMTP when configured.
Hidden Gems | FBLA 2026
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Load config from config.py if present, else use env vars
def _get_config():
    try:
        import config
        return {
            "host": getattr(config, "SMTP_HOST", None) or os.environ.get("SMTP_HOST", "").strip(),
            "port": getattr(config, "SMTP_PORT", None) or os.environ.get("SMTP_PORT", "587"),
            "user": getattr(config, "SMTP_USER", None) or os.environ.get("SMTP_USER", "").strip(),
            "password": getattr(config, "SMTP_PASSWORD", None) or os.environ.get("SMTP_PASSWORD", "").strip(),
            "from_email": getattr(config, "FROM_EMAIL", None) or os.environ.get("FROM_EMAIL", "").strip(),
            "from_name": getattr(config, "FROM_NAME", None) or os.environ.get("FROM_NAME", "Hidden Gems"),
        }
    except ImportError:
        return {
            "host": os.environ.get("SMTP_HOST", "").strip(),
            "port": os.environ.get("SMTP_PORT", "587"),
            "user": os.environ.get("SMTP_USER", "").strip(),
            "password": os.environ.get("SMTP_PASSWORD", "").strip(),
            "from_email": os.environ.get("FROM_EMAIL", "").strip(),
            "from_name": os.environ.get("FROM_NAME", "Hidden Gems"),
        }


def is_email_configured():
    """True if we have enough SMTP settings to try sending."""
    c = _get_config()
    return bool(c["host"] and c["user"] and c["password"] and c["from_email"])


def send_verification_email(to_email, code):
    """
    Send the verification code to the user's email.
    Returns (True, None) on success, (False, error_message) on failure.
    """
    if not is_email_configured():
        return False, "Email not configured"
    c = _get_config()
    try:
        port = int(c["port"])
    except (TypeError, ValueError):
        port = 587
    from_addr = c["from_email"] if not c["from_name"] else f"{c['from_name']} <{c['from_email']}>"
    subject = "Your Hidden Gems verification code"
    body = f"""Hello,

Your verification code for Hidden Gems is:

  {code}

Enter this code in the app to verify your email. The code is valid for this session.

If you didn't request this, you can ignore this email.

— Hidden Gems
"""
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(c["host"], port, timeout=10) as server:
            server.starttls()
            server.login(c["user"], c["password"])
            server.sendmail(c["from_email"], to_email, msg.as_string())
        return True, None
    except Exception as e:
        return False, str(e)


def send_password_reset_email(to_email, reset_link):
    """
    Send a password reset link to the user's email.
    Returns (True, None) on success, (False, error_message) on failure.
    """
    if not is_email_configured():
        return False, "Email not configured"
    c = _get_config()
    try:
        port = int(c["port"])
    except (TypeError, ValueError):
        port = 587
    from_addr = c["from_email"] if not c["from_name"] else f"{c['from_name']} <{c['from_email']}>"
    subject = "Reset Your Hidden Gems Password"
    body = f"""Hello,

You requested to reset your Hidden Gems password. Click the link below to set a new password:

{reset_link}

This link is valid for 1 hour. If you didn't request this, you can ignore this email.

— Hidden Gems
"""
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(c["host"], port, timeout=10) as server:
            server.starttls()
            server.login(c["user"], c["password"])
            server.sendmail(c["from_email"], to_email, msg.as_string())
        return True, None
    except Exception as e:
        return False, str(e)
