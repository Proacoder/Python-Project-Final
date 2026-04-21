import hashlib
import secrets
import re
from database import get_connection


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with a salt."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored hash."""
    try:
        salt, hashed = stored_hash.split(":")
        check = hashlib.sha256((password + salt).encode()).hexdigest()
        return check == hashed
    except Exception:
        return False


def validate_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit."
    return True, "OK"


def signup_user(username: str, email: str, password: str) -> tuple[bool, str]:
    """Register a new user. Returns (success, message)."""
    username = username.strip()
    email = email.strip().lower()

    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters."
    if not validate_email(email):
        return False, "Invalid email address."
    valid, msg = validate_password(password)
    if not valid:
        return False, msg

    conn = get_connection()
    try:
        taken_username = conn.execute(
            "SELECT id FROM users WHERE LOWER(username) = LOWER(?)", (username,)
        ).fetchone()
        if taken_username:
            return False, "That username is already taken. Please choose a different one."

        taken_email = conn.execute(
            "SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (email,)
        ).fetchone()
        if taken_email:
            return False, "An account with that email already exists."

        password_hash = hash_password(password)
        conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        return True, "Account created successfully!"
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()


def login_user(username: str, password: str) -> tuple[bool, dict | str]:
    """Authenticate a user. Returns (success, user_dict or error_message)."""
    username = username.strip()
    conn = get_connection()
    try:
        user = conn.execute(
            "SELECT id, username, email, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        if not user:
            return False, "Invalid username or password."
        if not verify_password(password, user["password_hash"]):
            return False, "Invalid username or password."
        return True, {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()
