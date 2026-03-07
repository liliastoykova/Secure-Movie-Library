import re

def validate_password_strength(password: str) -> str:
    errors = []

    if not re.search(r'[A-Z]', password):
        errors.append('at least one uppercase letter')
    if not re.search(r'[a-z]', password):
        errors.append('at least one lowercase letter')
    if not re.search(r'\d', password):
        errors.append('at least one digit')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('at least one special character')

    if errors:
        raise ValueError(f"Password must contain {', '.join(errors)}")

    return password
