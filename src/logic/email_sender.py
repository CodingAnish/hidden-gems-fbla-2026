"""
Email Sending Module - SMTP Configuration and Email Delivery

Handles sending transactional emails (verification, password reset) via SMTP.
Configuration can come from environment variables or config.py file.
Falls back gracefully if SMTP is not configured (for development).

Hidden Gems | FBLA 2026
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# ============================================
# SMTP CONFIGURATION
# ============================================

def _load_email_configuration():
    """
    Load SMTP configuration from config module or environment variables.
    
    Tries to import config.py first for development, falls back to environment.
    This allows flexible configuration management.
    
    Returns:
        dict: Configuration dictionary with keys:
            - host: SMTP server hostname
            - port: SMTP port (default: 587)
            - user: SMTP authentication username
            - password: SMTP authentication password
            - from_email: Email address to send from
            - from_name: Display name for sender (default: "Hidden Gems")
    """
    try:
        # Try to import config module from project root
        import config
        smtp_config = {
            "host": getattr(config, "SMTP_HOST", None) or os.environ.get("SMTP_HOST", "").strip(),
            "port": getattr(config, "SMTP_PORT", None) or os.environ.get("SMTP_PORT", "587"),
            "user": getattr(config, "SMTP_USER", None) or os.environ.get("SMTP_USER", "").strip(),
            "password": getattr(config, "SMTP_PASSWORD", None) or os.environ.get("SMTP_PASSWORD", "").strip(),
            "from_email": getattr(config, "FROM_EMAIL", None) or os.environ.get("FROM_EMAIL", "").strip(),
            "from_name": getattr(config, "FROM_NAME", None) or os.environ.get("FROM_NAME", "Hidden Gems"),
        }
    except ImportError:
        # Fallback to environment variables only
        smtp_config = {
            "host": os.environ.get("SMTP_HOST", "").strip(),
            "port": os.environ.get("SMTP_PORT", "587"),
            "user": os.environ.get("SMTP_USER", "").strip(),
            "password": os.environ.get("SMTP_PASSWORD", "").strip(),
            "from_email": os.environ.get("FROM_EMAIL", "").strip(),
            "from_name": os.environ.get("FROM_NAME", "Hidden Gems"),
        }
    
    return smtp_config


def is_email_configured():
    """
    Check if SMTP is properly configured and ready to send emails.
    
    Requires all of: host, user, password, from_email to be present.
    
    Returns:
        bool: True if SMTP can be used, False if not configured
    """
    email_config = _load_email_configuration()
    return bool(
        email_config["host"] and 
        email_config["user"] and 
        email_config["password"] and 
        email_config["from_email"]
    )


# ============================================
# EMAIL SENDING FUNCTIONS
# ============================================

def send_verification_email(recipient_email, verification_code):
    """
    Send email verification code to user during registration.
    
    Args:
        recipient_email (str): Email address to send to
        verification_code (str): 6-digit code user must enter to verify
    
    Returns:
        tuple: (success: bool, error_message: str or None)
            - On success: (True, None)
            - On failure: (False, error_description)
    """
    # Check if email is configured
    if not is_email_configured():
        return False, "Email service not configured"
    
    # Load SMTP configuration
    email_config = _load_email_configuration()
    
    # Parse SMTP port (convert string to int)
    try:
        smtp_port = int(email_config["port"])
    except (TypeError, ValueError):
        smtp_port = 587  # Default TLS port if parsing fails
    
    # Format sender address with optional display name
    if email_config["from_name"]:
        sender_address = f"{email_config['from_name']} <{email_config['from_email']}>"
    else:
        sender_address = email_config["from_email"]
    
    # Build email subject and body
    email_subject = "Your Hidden Gems Verification Code"
    email_body = f"""Hello,

Your verification code for Hidden Gems is:

  {verification_code}

Enter this code in the app to verify your email address. This code is valid for this session.

If you didn't create a Hidden Gems account, you can ignore this email.

— Hidden Gems Team
Richmond, Virginia
"""
    
    # Construct MIME email message
    email_message = MIMEMultipart()
    email_message["From"] = sender_address
    email_message["To"] = recipient_email
    email_message["Subject"] = email_subject
    email_message.attach(MIMEText(email_body, "plain"))
    
    # Attempt to send email via SMTP
    try:
        with smtplib.SMTP(email_config["host"], smtp_port, timeout=10) as smtp_server:
            # Upgrade connection to TLS encryption
            smtp_server.starttls()
            # Authenticate with SMTP server
            smtp_server.login(email_config["user"], email_config["password"])
            # Send email
            smtp_server.sendmail(
                email_config["from_email"], 
                recipient_email, 
                email_message.as_string()
            )
        return True, None
    except Exception as smtp_error:
        # Return error details for logging/debugging
        return False, str(smtp_error)


def send_password_reset_email(recipient_email, password_reset_link):
    """
    Send password reset link to user via email.
    
    Args:
        recipient_email (str): Email address to send to
        password_reset_link (str): Full URL link user clicks to reset password
    
    Returns:
        tuple: (success: bool, error_message: str or None)
            - On success: (True, None)
            - On failure: (False, error_description)
    """
    # Check if email is configured
    if not is_email_configured():
        return False, "Email service not configured"
    
    # Load SMTP configuration
    email_config = _load_email_configuration()
    
    # Parse SMTP port (convert string to int)
    try:
        smtp_port = int(email_config["port"])
    except (TypeError, ValueError):
        smtp_port = 587  # Default TLS port if parsing fails
    
    # Format sender address with optional display name
    if email_config["from_name"]:
        sender_address = f"{email_config['from_name']} <{email_config['from_email']}>"
    else:
        sender_address = email_config["from_email"]
    
    # Build email subject and body with reset link
    email_subject = "Reset Your Hidden Gems Password"
    email_body = f"""Hello,

You requested to reset your Hidden Gems password. Click the link below to set a new password:

{password_reset_link}

This link is valid for 1 hour. If you didn't request this, you can ignore this email.

— Hidden Gems Team
Richmond, Virginia
"""
    
    # Construct MIME email message
    email_message = MIMEMultipart()
    email_message["From"] = sender_address
    email_message["To"] = recipient_email
    email_message["Subject"] = email_subject
    email_message.attach(MIMEText(email_body, "plain"))
    
    # Attempt to send email via SMTP
    try:
        with smtplib.SMTP(email_config["host"], smtp_port, timeout=10) as smtp_server:
            # Upgrade connection to TLS encryption
            smtp_server.starttls()
            # Authenticate with SMTP server
            smtp_server.login(email_config["user"], email_config["password"])
            # Send email
            smtp_server.sendmail(
                email_config["from_email"], 
                recipient_email, 
                email_message.as_string()
            )
        return True, None
    except Exception as smtp_error:
        # Return error details for logging/debugging
        return False, str(smtp_error)
