from auth.hashing import verify_password
from repositories.users_repository import UserRepository

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, username: str, password: str):
        user = self.user_repo.get_user_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
