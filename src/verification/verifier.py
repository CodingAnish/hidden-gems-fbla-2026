"""
Verification module for bot prevention (math/code challenge) and audit logging.
"""
import random
import string
from src.database import queries


def generate_math_challenge():
    """Generate a simple math question. Returns (question, correct_answer)."""
    left_operand = random.randint(1, 15)
    right_operand = random.randint(1, 15)
    operator = random.choice(["+", "-"])
    if operator == "+":
        correct_answer = left_operand + right_operand
        question = f"What is {left_operand} + {right_operand}?"
    else:
        # Ensure non-negative subtraction for friendlier challenges.
        if left_operand < right_operand:
            left_operand, right_operand = right_operand, left_operand
        correct_answer = left_operand - right_operand
        question = f"What is {left_operand} - {right_operand}?"
    return question, str(correct_answer)


def generate_code_challenge():
    """Generate a 4-character code. Returns (question, correct_answer)."""
    verification_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"Enter the verification code: {verification_code}", verification_code


def get_challenge():
    """Return (question, correct_answer) using either math or code verification."""
    if random.random() < 0.5:
        return generate_math_challenge()
    return generate_code_challenge()


def verify_and_log(email, user_answer, question, correct_answer, context="login"):
    """
    Validate user_answer against correct_answer (case-insensitive for codes).
    Log each attempt to the verification_attempts table.
    Returns True if correct, False otherwise.
    """
    user_input = (user_answer or "").strip()
    expected_answer = (correct_answer or "").strip()
    is_code_challenge = any(char.isalpha() for char in expected_answer)
    # Allow case-insensitive matches for code challenges only.
    if is_code_challenge:
        success = user_input.lower() == expected_answer.lower()
    else:
        success = user_input == expected_answer
    verification_type = "code" if is_code_challenge else "math"
    queries.log_verification_attempt(
        email=email,
        verification_type=verification_type,
        question=question,
        correct_answer=correct_answer,
        user_answer=user_answer,
        success=success,
        context=context,
    )
    return success
