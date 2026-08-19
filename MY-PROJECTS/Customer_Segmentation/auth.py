import os
import re
import hashlib
import binascii

def hash_password(password: str) -> str:
    """Hashes a password with a unique cryptographic salt using PBKDF2-HMAC-SHA256."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(password: str, stored_password_hash: str) -> bool:
    """Verifies a password against the stored PBKDF2 hash."""
    try:
        salt = stored_password_hash[:64]
        stored_hash = stored_password_hash[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_hash
    except Exception:
        return False

def validate_email(email: str) -> bool:
    """Validates email format using regex."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip()))

def validate_registration(name: str, email: str, password: str, confirm_password: str):
    """Validates user registration input fields."""
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long."
    
    if not email or not validate_email(email):
        return False, "Please enter a valid email address."
        
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
        
    if password != confirm_password:
        return False, "Passwords do not match."
        
    return True, ""
