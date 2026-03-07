from typing import Literal
from pydantic import BaseModel, Field, EmailStr, field_validator

import utils.validate_password


class Movies(BaseModel):
    id: int
    title: str = Field(min_length=2, max_length=32)
    director: str | None
    release_year: int | None
    rating: float | None

class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=10)

class UserWithEmail(UserBase):
    email: str = Field(
        description="Valid email address, must be unique in the system",
        examples=["john@example.com"]
    )

class UserCreate(UserWithEmail):
    password: str = Field(min_length=2, max_length=16)

    @field_validator('password')
    @classmethod
    def validate_password(cls, p: str):
        return utils.validate_password.validate_password_strength(p)



