from auth.hashing import verify_password
from repositories.users_repository import get_user_by_username


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
