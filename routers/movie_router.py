from fastapi import APIRouter, status
from services.movie_service import *
from data.models import MovieCreate

movie_router = APIRouter(prefix="/movies")

@movie_router.post("/", status_code=status.HTTP_201_CREATED)
def create_movies(data: MovieCreate):
    movie_id = create_new_movie(data)
    return {"id": movie_id, "message": "Movie created."}

@movie_router.get("")
def get_all_movies(search: str | None = None, sort: str | None = None):
    return get_all(search, sort)

@movie_router.get("/{movie_id}")
def get_movies_by_id(movie_id: int):
    return get_by_id(movie_id)

@movie_router.put("/{movie_id}")
def update_movie(movie_id: int, data: MovieUpdate):
    return change_movie(movie_id, data)

@movie_router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    return remove_movie(movie_id)




