"""
Authentication module for reading list API.
Uses email-based authentication with tokens.
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# Store tokens in memory (in production, use a database)
# Format: {token: {"email": "...", "expires": datetime, "verified": bool}}
active_tokens = {}

# Configuration
AUTHORIZED_EMAIL = os.getenv("AUTHORIZED_EMAIL", "stephie.maths@icloud.com")
TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", "24"))


def generate_token():
    """Generate a secure random token."""
    return secrets.token_urlsafe(32)


def hash_token(token):
    """Hash a token for secure comparison."""
    return hashlib.sha256(token.encode()).hexdigest()


def create_token(email):
    """Create an authentication token for an email."""
    if email != AUTHORIZED_EMAIL:
        return None, "Email not authorized"
    
    token = generate_token()
    active_tokens[token] = {
        "email": email,
        "created": datetime.now(),
        "expires": datetime.now() + timedelta(hours=TOKEN_EXPIRY_HOURS),
        "verified": False
    }
    
    return token, None


def verify_token(token):
    """Verify a token is valid and not expired."""
    if not token or token not in active_tokens:
        return False, "Invalid token"
    
    token_data = active_tokens[token]
    
    if datetime.now() > token_data["expires"]:
        del active_tokens[token]
        return False, "Token expired"
    
    if not token_data.get("verified"):
        return False, "Token not verified"
    
    return True, None


def mark_token_verified(token):
    """Mark a token as verified (after 2FA)."""
    if token in active_tokens:
        active_tokens[token]["verified"] = True
        return True
    return False


def extract_token(request_obj):
    """Extract token from request headers."""
    auth_header = request_obj.headers.get("Authorization", "")
    
    if not auth_header.startswith("Bearer "):
        return None
    
    return auth_header[7:]  # Remove "Bearer " prefix


def require_auth(f):
    """Decorator to require valid authentication token."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = extract_token(request)
        
        if not token:
            return jsonify({"error": "Missing authorization token"}), 401
        
        is_valid, error_msg = verify_token(token)
        if not is_valid:
            return jsonify({"error": error_msg}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
