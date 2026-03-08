from fastapi import HTTPException
from data.models import UserCreate
from repositories.users_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, user_data: UserCreate):
        if self.user_repo.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=400,
                detail="Username already taken. Please choose a different username."
            )
        user_data.role = "USER"

        self.user_repo.create_user(user_data)

        user = self.user_repo.get_user_by_username(user_data.username)

        return user

