"""
Authentication logic - password hashing and email login validation.
Hidden Gems | FBLA 2026
"""
import hashlib
import re
import random
from src.database import queries

# Simple salt for local app (stored in code; no internet)
SALT = b"HiddenGems_FBLA2026"


def hash_password(password):
    """Return SHA-256 hash of salt + password."""
    if not password:
        return ""
    h = hashlib.sha256(SALT + password.encode("utf-8"))
    return h.hexdigest()


def is_valid_email(email):
    """Basic email format validation."""
    if not email or not isinstance(email, str):
        return False
    email = email.strip().lower()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_username(s):
    """Username: 3–30 chars, letters, numbers, underscore only."""
    if not s or not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) < 3 or len(s) > 30:
        return False
    return all(c.isalnum() or c == "_" for c in s)


def is_valid_password(password):
    """
    Password validation: 8+ characters, 1+ uppercase, 1+ number, 1+ symbol.
    Returns (True, None) or (False, error_message).
    """
    if not password or not isinstance(password, str):
        return False, "Password is required."
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\,.<>?/]", password):
        return False, "Password must contain at least one symbol (!@#$%^&* etc)."
    
    return True, None


def validate_login(identifier, password):
    """
    Validate email-or-username + password against DB. Requires email to be verified.
    Returns (True, user_dict) on success, (False, error_message) on failure.
    user_dict includes id, email, username (display name).
    """
    if not identifier or not str(identifier).strip():
        return False, "Email or username is required."
    if not password:
        return False, "Password is required."
    user = queries.user_by_email_or_username(identifier)
    if not user:
        return False, "No account found with that email or username."
    if user["password_hash"] != hash_password(password):
        return False, "Incorrect password."
    if not user.get("email_verified", 1):
        return False, "EMAIL_NOT_VERIFIED"
    return True, {
        "id": user["id"],
        "email": user["email"],
        "username": user.get("username") or user["email"],
    }


def generate_verification_code():
    """Generate a 6-digit verification code."""
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


def register_user(username, email, password):
    """
    Create a new user. Returns (True, user_id) or (False, error_message).
    """
    if not username or not str(username).strip():
        return False, "Username is required."
    if not is_valid_username(username):
        return False, "Username must be 3–30 characters (letters, numbers, underscore only)."
    if not email or not str(email).strip():
        return False, "Email is required."
    valid_pwd, pwd_error = is_valid_password(password)
    if not valid_pwd:
        return False, pwd_error
    if not is_valid_email(email):
        return False, "Please enter a valid email address."
    uid = queries.create_user(username.strip().lower(), email.strip().lower(), hash_password(password))
    if uid is None:
        return False, "An account with this email or username already exists."
    return True, uid
