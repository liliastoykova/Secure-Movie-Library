import os
import jwt
from datetime import datetime, timezone, timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if len(SECRET_KEY) < 32:
    raise RuntimeError(
        f"CRITICAL: JWT_SECRET_KEY must be at least 32 characters long for security.\n"
        f"Current length: {len(SECRET_KEY)} characters.\n"
        f"Generate a secure key with: openssl rand -hex 32"
    )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

