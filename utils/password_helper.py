# =====================================================
# Password Helper
# Handles hashing and verifying admin passwords
# Uses SHA-256 (one-way hashing — cannot be reversed)
# =====================================================

import hashlib


# =====================================================
# HASH PASSWORD
# =====================================================

def hash_password(password):
    """
    Takes a plain-text password and returns its SHA-256 hash.
    This hash is stored in the database — never the raw password.
    """

    return hashlib.sha256(password.encode()).hexdigest()


# =====================================================
# VERIFY PASSWORD
# =====================================================

def verify_password(input_password, stored_password):
    """
    Hashes the input password and compares it to the stored hash.
    Returns True if they match, False otherwise.
    """

    # HASH THE INPUT PASSWORD
    hashed_input = hashlib.sha256(
        input_password.encode()
    ).hexdigest()

    # COMPARE WITH STORED HASH
    return hashed_input == stored_password