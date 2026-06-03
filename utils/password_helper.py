import hashlib


# ==========================================
# HASH PASSWORD
# ==========================================

def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()


# ==========================================
# VERIFY PASSWORD
# ==========================================

def verify_password(input_password, stored_password):

    hashed_input = hashlib.sha256(
        input_password.encode()
    ).hexdigest()

    return hashed_input == stored_password