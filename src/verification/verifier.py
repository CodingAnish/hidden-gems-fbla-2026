"""
Verification module - bot prevention (math/code challenge) and logging to DB.
Hidden Gems | FBLA 2026
"""
import random
import string
from src.database import queries


def generate_math_challenge():
    """Generate a simple math question. Returns (question_string, correct_answer_string)."""
    a = random.randint(1, 15)
    b = random.randint(1, 15)
    op = random.choice(["+", "-"])
    if op == "+":
        ans = a + b
        q = f"What is {a} + {b}?"
    else:
        if a < b:
            a, b = b, a
        ans = a - b
        q = f"What is {a} - {b}?"
    return q, str(ans)


def generate_code_challenge():
    """Generate a 4-character code. Returns (question_string, correct_answer_string)."""
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"Enter the verification code: {code}", code


def get_challenge():
    """Return (question, correct_answer) - either math or code."""
    if random.random() < 0.5:
        return generate_math_challenge()
    return generate_code_challenge()


def verify_and_log(email, user_answer, question, correct_answer, context="login"):
    """
    Check user_answer against correct_answer (case-insensitive for code).
    Log attempt to verification_attempts table.
    Returns True if correct, False otherwise.
    """
    user_clean = (user_answer or "").strip()
    correct_clean = (correct_answer or "").strip()
    # For codes, allow case-insensitive
    success = user_clean == correct_clean or user_clean.lower() == correct_clean.lower()
    vtype = "code" if any(c in correct_answer for c in string.ascii_uppercase) else "math"
    queries.log_verification_attempt(
        email=email,
        verification_type=vtype,
        question=question,
        correct_answer=correct_answer,
        user_answer=user_answer,
        success=success,
        context=context,
    )
    return success
