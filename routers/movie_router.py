from fastapi import APIRouter, status
from fastapi.params import Depends
from auth.dependencies import require_admin, get_current_user, get_movie_service
from services.movie_service import *
from data.models import MovieCreate
from fastapi import BackgroundTasks

movie_router = APIRouter(prefix="/movies")

@movie_router.post("/", status_code=status.HTTP_201_CREATED)
def create_movies(data: MovieCreate,
                  background_tasks: BackgroundTasks,
                  user = Depends(require_admin),
                  movie_service: MovieService = Depends(get_movie_service)):

    movie_id = movie_service.create_new_movie(data)

    background_tasks.add_task(movie_service.enrich_movie_rating, movie_id, data.title)

    return {"id": movie_id, "message": "Movie created."}

@movie_router.get("")
def get_all_movies(search: str | None = None, sort: str | None = None,
                   user = Depends(get_current_user),
                   movie_service: MovieService = Depends(get_movie_service)):
    return movie_service.get_all(search, sort)

@movie_router.get("/{movie_id}")
def get_movies_by_id(movie_id: int,
                     user = Depends(get_current_user),
                     movie_service: MovieService = Depends(get_movie_service)):
    return movie_service.get_by_id(movie_id)

@movie_router.put("/{movie_id}")
def update_movie(movie_id: int, data: MovieUpdate,
                 user = Depends(require_admin),
                 movie_service: MovieService = Depends(get_movie_service)):
    return movie_service.change_movie(movie_id, data)

@movie_router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int,
                 user = Depends(require_admin),
                 movie_service: MovieService = Depends(get_movie_service)):
    return movie_service.remove_movie(movie_id)




