"""
Email Sending Module - SendGrid Email Delivery

Handles sending transactional emails (verification, password reset) via SendGrid API.
Configuration can come from environment variables or config.py file.
Falls back gracefully if SendGrid is not configured (for development).

Emails are sent asynchronously in background threads to avoid blocking the request.

Hidden Gems | FBLA 2026
"""
import os
import threading

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False

# ============================================
# EMAIL CONFIGURATION
# ============================================

def _load_email_configuration():
    """
    Load email configuration from config module or environment variables.
    
    Tries to import config.py first for development, falls back to environment.
    This allows flexible configuration management.
    
    Returns:
        dict: Configuration dictionary with keys:
            - api_key: SendGrid API key
            - from_email: Email address to send from
            - from_name: Display name for sender (default: "Hidden Gems")
    """
    try:
        # Try to import config module from project root
        import config
        email_config = {
            "api_key": getattr(config, "SENDGRID_API_KEY", None) or os.environ.get("SENDGRID_API_KEY", "").strip(),
            "from_email": getattr(config, "FROM_EMAIL", None) or os.environ.get("FROM_EMAIL", "hiddengems.official26@gmail.com").strip(),
            "from_name": getattr(config, "FROM_NAME", None) or os.environ.get("FROM_NAME", "Hidden Gems"),
        }
    except ImportError:
        # Fallback to environment variables only
        email_config = {
            "api_key": os.environ.get("SENDGRID_API_KEY", "").strip(),
            "from_email": os.environ.get("FROM_EMAIL", "hiddengems.official26@gmail.com").strip(),
            "from_name": os.environ.get("FROM_NAME", "Hidden Gems"),
        }
    
    return email_config


def is_email_configured():
    """
    Check if SendGrid is properly configured and ready to send emails.
    
    Requires SendGrid library and API key to be present.
    
    Returns:
        bool: True if SendGrid can be used, False if not configured
    """
    if not SENDGRID_AVAILABLE:
        return False
    
    email_config = _load_email_configuration()
    return bool(email_config["api_key"] and email_config["from_email"])


# ============================================
# EMAIL SENDING FUNCTIONS
# ============================================

def _send_email_async(to_email, subject, body, email_config):
    """
    Send email asynchronously in a background thread.
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        body (str): Email body text
        email_config (dict): Email configuration with api_key, from_email, from_name
    
    Returns:
        None (runs in background)
    """
    try:
        message = Mail(
            from_email=(email_config["from_email"], email_config["from_name"]),
            to_emails=to_email,
            subject=subject,
            plain_text_content=body
        )
        
        sg = SendGridAPIClient(email_config["api_key"])
        response = sg.send(message)
        
        if response.status_code in [200, 201, 202]:
            print(f"✓ Email sent to {to_email}")
        else:
            print(f"✗ Email failed to {to_email} (status {response.status_code})")
            
    except Exception as e:
        print(f"✗ Email error for {to_email}: {str(e)}")


def send_verification_email(recipient_email, verification_code):
    """
    Send email verification code to user during registration.
    
    ASYNC: Email is sent in background thread - returns immediately without blocking.
    
    Args:
        recipient_email (str): Email address to send to
        verification_code (str): 6-digit code user must enter to verify
    
    Returns:
        tuple: (success: bool, error_message: str or None)
            - Immediate: (True, None) - email queued for background sending
            - If not configured: (False, error_description)
    """
    # Check if email is configured
    if not is_email_configured():
        return False, "Email service not configured"
    
    # Load email configuration
    email_config = _load_email_configuration()
    
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
    
    # Send email in background thread (non-blocking)
    thread = threading.Thread(
        target=_send_email_async,
        args=(recipient_email, email_subject, email_body, email_config),
        daemon=True
    )
    thread.start()
    
    # Return immediately - email is being sent in background
    return True, None


def send_password_reset_email(recipient_email, password_reset_link):
    """
    Send password reset link to user via email.
    
    ASYNC: Email is sent in background thread - returns immediately without blocking.
    
    Args:
        recipient_email (str): Email address to send to
        password_reset_link (str): Full URL link user clicks to reset password
    
    Returns:
        tuple: (success: bool, error_message: str or None)
            - Immediate: (True, None) - email queued for background sending
            - If not configured: (False, error_description)
    """
    # Check if email is configured
    if not is_email_configured():
        return False, "Email service not configured"
    
    # Load email configuration
    email_config = _load_email_configuration()
    
    # Build email subject and body with reset link
    email_subject = "Reset Your Hidden Gems Password"
    email_body = f"""Hello,

You requested to reset your Hidden Gems password. Click the link below to set a new password:

{password_reset_link}

This link is valid for 1 hour. If you didn't request this, you can ignore this email.

— Hidden Gems Team
Richmond, Virginia
"""
    
    # Send email in background thread (non-blocking)
    thread = threading.Thread(
        target=_send_email_async,
        args=(recipient_email, email_subject, email_body, email_config),
        daemon=True
    )
    thread.start()
    
    # Return immediately - email is being sent in background
    return True, None
