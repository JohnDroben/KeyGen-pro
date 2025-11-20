import string
import secrets

def generate_secure_password(length, use_upper, use_lower, use_digits, use_symbols):
    char_pool = ""
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not char_pool:
        return None

    return ''.join(secrets.choice(char_pool) for _ in range(length))

def check_password_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1

    if score <= 2:
        return ("Слабый", "red")
    elif score <= 4:
        return ("Средний", "yellow")
    else:
        return ("Сильный", "green")
