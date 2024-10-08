from hashlib import sha512

def hash_password(password: str) -> str:
    return sha512(password.encode()).hexdigest()