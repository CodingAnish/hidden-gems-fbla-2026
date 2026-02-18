"""
Authentication and Authorization Logic

Handles user registration validation, login authentication, and password hashing.
All passwords are hashed with SHA-256 and a static salt (suitable for local development).

Hidden Gems | FBLA 2026
"""
import hashlib
import re
import random
from src.database import queries

# Static salt for password hashing (used with local app)
# In production, consider using bcrypt or argon2 instead of SHA-256
PASSWORD_SALT = b"HiddenGems_FBLA2026"


def hash_password(password):
    """
    Hash a password using SHA-256 with a static salt.
    
    Args:
        password (str): The plain-text password to hash
    
    Returns:
        str: Hexadecimal SHA-256 hash of salt + password
    """
    if not password:
        return ""
    password_hash = hashlib.sha256(PASSWORD_SALT + password.encode("utf-8"))
    return password_hash.hexdigest()


def is_valid_email(email):
    """
    Validate email format using regex pattern.
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if email matches pattern, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip().lower()
    # RFC 5322 simplified pattern for basic validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_pattern, email))


def is_valid_username(username):
    """
    Validate username format: 3-30 characters, alphanumeric and underscore only.
    
    Args:
        username (str): Username to validate
    
    Returns:
        bool: True if username meets requirements, False otherwise
    """
    if not username or not isinstance(username, str):
        return False
    
    username = username.strip()
    
    # Check length requirements
    if len(username) < 3 or len(username) > 30:
        return False
    
    # Check character restrictions (letters, numbers, underscore only)
    return all(c.isalnum() or c == "_" for c in username)


def is_valid_password(password):
    """
    Validate password strength requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter (A-Z)
    - At least 1 number (0-9)
    - At least 1 special symbol (!@#$%^&* etc)
    
    Args:
        password (str): Password to validate
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required."
    
    # Check minimum length
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    
    # Check for uppercase letter
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    
    # Check for number
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    
    # Check for special symbol
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\,.<>?/]", password):
        return False, "Password must contain at least one special symbol (!@#$%^&* etc)."
    
    return True, None


def validate_login(identifier, password):
    """
    Authenticate user with email/username and password.
    
    Validates that:
    1. User account exists
    2. Password matches stored hash
    3. Email address has been verified
    
    Args:
        identifier (str): Email address or username
        password (str): Plain-text password to verify
    
    Returns:
        tuple: (success: bool, result: dict or str)
            - On success: (True, {id, email, username})
            - On failure: (False, error_message)
            - If email not verified: (False, "EMAIL_NOT_VERIFIED")
    """
    # Validate input is provided
    if not identifier or not str(identifier).strip():
        return False, "Email or username is required."
    
    if not password:
        return False, "Password is required."
    
    # Look up user by email or username
    user = queries.user_by_email_or_username(identifier)
    if not user:
        return False, "No account found with that email or username."
    
    # Verify password hash matches
    if user["password_hash"] != hash_password(password):
        return False, "Incorrect password."
    
    # Check if email has been verified (required for login)
    if not user.get("email_verified", 1):
        return False, "EMAIL_NOT_VERIFIED"
    
    # Return user object with standardized fields
    return True, {
        "id": user["id"],
        "email": user["email"],
        "username": user.get("username") or user["email"],
    }


def generate_verification_code():
    """
    Generate a random 6-digit numeric verification code.
    
    Used for email verification and password reset links.
    
    Returns:
        str: Six-digit verification code (e.g., "384729")
    """
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


def register_user(username, email, password):
    """
    Create a new user account after validation.
    
    Validates all input before creating account.
    Prevents duplicate emails or usernames.
    
    Args:
        username (str): Desired username
        email (str): Email address
        password (str): Plain-text password (will be hashed)
    
    Returns:
        tuple: (success: bool, result: int or str)
            - On success: (True, new_user_id)
            - On failure: (False, error_message)
    """
    # Validate username is provided and meets requirements
    if not username or not str(username).strip():
        return False, "Username is required."
    
    if not is_valid_username(username):
        return False, "Username must be 3–30 characters (letters, numbers, underscore only)."
    
    # Validate email is provided and valid format
    if not email or not str(email).strip():
        return False, "Email is required."
    
    # Validate password strength
    password_is_valid, password_error = is_valid_password(password)
    if not password_is_valid:
        return False, password_error
    
    # Validate email format
    if not is_valid_email(email):
        return False, "Please enter a valid email address."
    
    # Create user in database (hash password before storing)
    new_user_id = queries.create_user(
        username.strip().lower(), 
        email.strip().lower(), 
        hash_password(password)
    )
    
    # Check if creation failed (duplicate email/username)
    if new_user_id is None:
        return False, "An account with this email or username already exists."
    
    return True, new_user_id
