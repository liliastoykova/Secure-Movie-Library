from typing import Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict
from utils.validate_password import validate_password_strength
from utils.validate_year import validate_release_year


class Movie(BaseModel):
    id: int
    title: str = Field(min_length=2, max_length=32)
    director: str | None
    release_year: int | None
    rating: float | None

class MovieCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Up",
                "director": "Pete Docter",
                "release_year": 2009
            }
        }
    )

    title: str = Field(min_length=2, max_length=32)
    director: str | None = Field(default=None, min_length=2, max_length=50)
    release_year: int | None = None

    @field_validator('release_year')
    @classmethod
    def validate_year(cls, year):
        return validate_release_year(year)

class MovieUpdate(BaseModel):
    title: str | None = Field(default=None,min_length=2, max_length=32)
    director: str | None = Field(default=None,min_length=2, max_length=50)
    release_year: int | None = None

    @field_validator('release_year')
    @classmethod
    def validate_year(cls, year):
        return validate_release_year(year)


class UserBase(BaseModel):
    username: str = Field(min_length=2,
                          max_length=10,
                          description="Unique username for the user. Cannot be changed after registration.",
                          examples=["johndoe", "alice_2024"]
                          )
    role: Literal["USER", "ADMIN"]

class UserCreate(UserBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "lilia",
                "password": "Securepass123!",
                "role": "USER"
            }
        }
    )
    password: str = Field(min_length=2, max_length=16)

    @field_validator('password')
    @classmethod
    def validate_password(cls, p: str):
        return validate_password_strength(p)

class User(BaseModel):
    id: int
    username: str = Field(min_length=2, max_length=10)
    password: str
    role: Literal["USER", "ADMIN"]


