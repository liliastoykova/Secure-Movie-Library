from fastapi import HTTPException
from data.models import UserCreate, User
from repositories.users_repository import get_user_by_username, create_user


def register_user(user_data: UserCreate):
    if get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username already taken. Please choose a different username."
        )
    user_data.role = "USER"

    user = create_user(user_data)

    return User(**user.model_dump())

