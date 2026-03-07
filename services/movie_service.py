from fastapi import HTTPException
from data.models import MovieCreate, MovieUpdate
from repositories.movies_repository import *


def create_new_movie(data: MovieCreate):
    movie_exists = get_movie_by_title(data.title)

    if movie_exists:
        raise HTTPException(409, "Movie already exists")

    movie_id = create_movie(data.title, data.director, data.release_year)
    return movie_id

def get_all(search: str | None, sort: str | None):
    return get_movies(search, sort)

def get_by_id(movie_id: int):
    movie = get_movie_by_id(movie_id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found.")

    return movie

def change_movie(movie_id: int, data: MovieUpdate):
    movie = get_movie_by_id(movie_id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found.")

    title = data.title if data.title is not None else movie.title
    director = data.director if data.director is not None else movie.director
    release_year = data.release_year if data.release_year is not None else movie.release_year

    update_movie(movie_id, title, director, release_year)

    return {"message": "Movie updated."}

def remove_movie(movie_id: int):
    movie = get_movie_by_id(movie_id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found.")

    delete_movie(movie.id)
