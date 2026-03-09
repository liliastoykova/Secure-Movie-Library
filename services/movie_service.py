from fastapi import HTTPException
from data.models import MovieCreate, MovieUpdate
from repositories.movies_repository import *

class MovieService:
    def __init__(self, movie_repo: MovieRepository):
        self.movie_repo = movie_repo

    def create_new_movie(self, data: MovieCreate):
        movie_exists = self.movie_repo.get_movie_by_title_and_year(data.title, data.release_year)

        if movie_exists:
            raise HTTPException(409, "Movie already exists")

        movie_id = self.movie_repo.create_movie(data.title, data.director, data.release_year)
        return movie_id

    def get_all(self, search: str | None, sort: str | None):
        return self.movie_repo.get_movies(search, sort)

    def get_by_id(self, movie_id: int):
        movie = self.movie_repo.get_movie_by_id(movie_id)

        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found.")

        return movie

    def change_movie(self, movie_id: int, data: MovieUpdate):
        movie = self.movie_repo.get_movie_by_id(movie_id)

        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found.")

        title = data.title if data.title is not None else movie.title
        director = data.director if data.director is not None else movie.director
        release_year = data.release_year if data.release_year is not None else movie.release_year

        existing = self.movie_repo.get_movie_by_title_and_year(title, release_year)

        if existing and existing != movie_id:
            raise HTTPException(status_code=409, detail="Movie with this title and year already exists.")

        self.movie_repo.update_movie(movie_id, title, director, release_year)

        return {"message": "Movie updated."}

    def remove_movie(self, movie_id: int):
        movie = self.movie_repo.get_movie_by_id(movie_id)

        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found.")

        self.movie_repo.delete_movie(movie.id)
