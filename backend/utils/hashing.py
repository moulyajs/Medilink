import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    """
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )