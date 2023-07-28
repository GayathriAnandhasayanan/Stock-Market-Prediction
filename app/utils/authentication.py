# app/utils/authentication.py
import hashlib


def get_password_hash(password):
    hashed_password = hashlib.md5(str(password).encode())
    return hashed_password.hexdigest()[:15]  # Limit the length to 15 characters

