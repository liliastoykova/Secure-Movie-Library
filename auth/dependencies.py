from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from data.models import TokenData
from auth.jwt_handler import SECRET_KEY, ALGORITHM
from repositories.movies_repository import MovieRepository
from repositories.users_repository import UserRepository
from services.auth_service import AuthService
from services.movie_service import MovieService
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_movie_repository():
    return MovieRepository()

def get_user_repository():
    return UserRepository()

def get_movie_service(movie_repo: MovieRepository = Depends(get_movie_repository)):
    return MovieService(movie_repo)

def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)

def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)):
    return AuthService(user_repo)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def require_admin(current_user = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required."
        )
    return current_user