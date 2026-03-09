import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException
from data.models import Movie, MovieUpdate, MovieCreate
from services.movie_service import MovieService


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

class TestGetMovieByID(unittest.TestCase):
    def test_nonexistent_movie_returns_404(self):
        service, repo = _make_service()
        repo.get_movie_by_id.return_value = None

        with self.assertRaises(HTTPException) as ctx:
            service.get_by_id(99)
        self.assertEqual(ctx.exception.status_code, 404)


    def test_get_movie_by_id_returns_movie(self):
        service, repo = _make_service()
        data = _make_movie()
        repo.get_movie_by_id.return_value = data

        result = service.get_by_id(6)

        self.assertEqual(result, data)


class TestChangeMovie(unittest.TestCase):
    def test_movie_updates(self):
        service, repo = _make_service()
        data = _make_movie()

        repo.get_movie_by_id.return_value = data

        repo.get_movie_by_title_and_year.return_value = None

        result = service.change_movie(7, MovieUpdate(title="Changed title", release_year=2002))

        self.assertEqual({"message": "Movie updated."}, result)

    def test_movie_does_not_update_when_it_already_exists(self):
        service, repo = _make_service()
        data = _make_movie()

        repo.get_movie_by_id.return_value = data

        repo.get_movie_by_title_and_year.return_value = data

        with self.assertRaises(HTTPException) as ctx:
            service.change_movie(7, MovieUpdate(title="Movie update"))
        self.assertEqual(ctx.exception.status_code, 409)

class TestDeleteMovie(unittest.TestCase):
    def test_movie_is_removed(self):
        service, repo = _make_service()

        repo.get_movie_by_id.return_value = Movie(
            id=7,
            title="Movie",
            director="Pete",
            release_year=2010,
            rating=None
        )

        service.remove_movie(7)
        repo.delete_movie.assert_called_once_with(7)



