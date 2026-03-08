import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException
from data.models import Movie, MovieUpdate, MovieCreate, UserCreate, User
from services.movie_service import MovieService
from repositories.movies_repository import MovieRepository

def _make_user(id=5, role="USER"):
    return User(id=id,
                username="lilia1",
                password="123Asr!",
                role=role)

def _make_movie():
    return MovieCreate(title="MovieTest",
                       director="Pete",
                       release_year=2010,
                       )
def _make_service():
    movie_repo = MagicMock()
    return MovieService(movie_repo), movie_repo

class TestCreateTopic(unittest.TestCase):
    def test_create_returns_new_id(self):
        service, repo = _make_service()

        repo.get_movie_by_title_and_year.return_value = None
        repo.create_movie.return_value = 6

        data = _make_movie()

        result = service.create_new_movie(data)

        self.assertEqual(result, 6)
        repo.create_movie.assert_called_once_with("MovieTest", "Pete", 2010)

    def test_create_returns_409_movie_exists(self):
        service, repo = _make_service()

        repo.get_movie_by_title_and_year.return_value = 6
        repo.create_movie.return_value = 6

        data = _make_movie()

        with self.assertRaises(HTTPException) as ctx:
            service.create_new_movie(data)
        self.assertEqual(ctx.exception.status_code, 409)



