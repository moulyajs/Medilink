import random


def generate_otp() -> str:
    """
    Generate a random 6-digit OTP.
    """
    return str(random.randint(100000, 999999))