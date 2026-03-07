from fastapi import APIRouter, status
from services.movie_service import get_all, create_new_movie
from data.models import MovieCreate

movie_router = APIRouter(prefix="/movies")

@movie_router.get("")
def get_all_movies(search: str | None = None, sort: str | None = None):
    return get_all(search, sort)

@movie_router.post("/")
def create_movies(data: MovieCreate):
    movie_id = create_new_movie(data)
    return {"id": movie_id, "message": "Movie created."}




